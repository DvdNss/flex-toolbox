"""

    PROJECT: flex_toolbox
    FILENAME: pull.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import json
from typing import List

import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

from VARIABLES import DEFAULT_GROOVY_SCRIPT
from src.env import get_default_env
from src.utils import create_folder

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. session
session = requests.Session()


def pull_command_func(args):
    """Action on pull command. """

    if args.config_item == "actions":
        get_items(config_item='actions', sub_items=['configuration'], filters=args.filters)


def get_items(config_item: str, sub_items: List[str] = [], filters: List[str] = []) -> dict:
    """
    Get items from an env using public API.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param sub_items: sub items to retrieve for item_name
    :param filters: filters to apply

    :return: dict['item_name': {item_config}]
    """

    # Init. function variables
    offset = 0
    batch_size = 100
    items = []

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # Get item total count
    total_count_request = f"{env['url']}/api/{config_item};limit=1;offset=0;{';'.join(filters) if filters else ''}"
    total_count = session.request("GET", total_count_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    if 'errors' in total_count:
        raise Exception(
            f"\n\nError while sending {total_count_request}. \nError message: {total_count['errors']['error']} ")

    total_count = total_count['totalCount']

    # Sequentially get all items (batch_size at a time)
    for _ in tqdm(range(0, int(total_count / batch_size) + 1), desc=f"Retrieving {config_item}"):

        try:
            # Get batch of items from API
            batched_item_request = f"{env['url']}/api/{config_item};limit={str(batch_size)};offset={str(offset)};{';'.join(filters) if filters else ''}"
            items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

            if 'errors' in items_batch:
                raise Exception(f"\n\nError while sending {batched_item_request}. \nError message: {items_batch['errors']['error']} ")

            # Add batch of items to the list
            items.extend(items_batch[config_item])

            # Incr. offset
            offset = offset + batch_size
        except KeyError as e:
            print(
                f"Either empty result from API or exact same number for totalCount and batch_size. Error is: {e}. Skipping.")

    # Convert list of items to dict
    items_dict = {}
    for item in items:
        items_dict[item['name']] = item  # item_name: item_config

    # Sort items dict by name (ignoring case)
    sorted_items_dict = {i: items_dict[i] for i in sorted(list(items_dict.keys()), key=lambda s: s.casefold())}

    # Get all items sub_items from API
    for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} {sub_items}"):
        for sub_item in sub_items:
            sub_item_request = f"{env['url']}/api/{config_item}/{str(items_dict[item]['id'])}/{sub_item}"
            items_dict[item][sub_item] = session.request("GET", sub_item_request, headers=HEADERS, auth=auth,
                                                         data=PAYLOAD).json() if sub_item != "body" else \
                session.request("GET", sub_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).content.decode(
                    "utf-8", "ignore").strip()

    # create retrieved objects
    for item in sorted_items_dict:

        # create config_item folder
        create_folder(item, ignore_error=True)

        # create groovy script
        if sorted_items_dict[item]['type']['name'] in ['script', 'decision']:

            # script in action
            try:
                create_script(item, sorted_items_dict[item])

            # no script in action
            except:
                print(f"Something went wrong while trying to retrieve {item} script.. Default script will be created instead.")
                with open(f"{item}/script.groovy", "w") as groovy_file:
                    groovy_file.write(DEFAULT_GROOVY_SCRIPT)

        # create or overwrite item config_file
        with open(f"{item}/config.json", "w") as config_file:
            json.dump(obj=sorted_items_dict[item], fp=config_file, indent=4)

    print(f"{config_item} have been pulled. ")

    # Add line break for UI
    print("")

    return sorted_items_dict


def create_script(item_name, item_config):
    """
    Create groovy script with according imports and plugins.

    :param item_name: script name
    :param item_config: script config
    :return:
    """

    imports = ["import com.ooyala.flex.plugins.PluginCommand\n"]
    script = "class Script extends PluginCommand {\n\t<&code>\n}"

    try:
        imports.extend(['import ' + imp['value'] + '\n' for imp in item_config['configuration']['instance']['internal-script']['script-import']])
    except:
        pass

    try:
        script = script.replace("<&code>", item_config['configuration']['instance']['internal-script']['script-content'].replace("\r\n", "\n\t"))
    except:
        script = script.replace("<&code>", "")

    content = f"{''.join(imports)}\n{script}"

    with open(f"{item_name}/script.groovy", "w") as groovy_file:
        groovy_file.write(content)
