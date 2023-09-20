"""

    PROJECT: flex_toolbox
    FILENAME: utils.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import os
import urllib.parse
from typing import List

import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

from src.env import get_default_env

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. session
session = requests.Session()


def create_folder(folder_name: str, ignore_error: bool = False):
    """
    Create folder or return error if already exists.

    :param folder_name: folder name
    :param ignore_error: whether to ignore folder already exists or not

    :return: True if created, False if error
    """

    try:
        os.mkdir(folder_name)
        # print(f"Folder {folder_name} was created. ")
        return True
    except FileExistsError:
        if ignore_error:
            return True
        else:
            print(f"Folder {folder_name} already exists. ")
        return False


def get_items(config_item: str, sub_items: List[str] = [], filters: List[str] = [], prefix: str = 'api') -> dict:
    """
    Get items from an env using public API.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param sub_items: sub items to retrieve for item_name
    :param filters: filters to apply
    :param prefix: prefix to apply in the request URL

    :return: dict['item_name': {item_config}]
    """

    # Init. function variables
    offset = 0
    batch_size = 100
    items = []

    # encode fql
    if filters:
        for idx, filter in enumerate(filters):
            if "fql=" in filter:
                filters[idx] = "fql=" + urllib.parse.quote(filter.replace("fql=", ""))

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # Get total count
    total_count_request = f"{env['url']}/{prefix}/{config_item};offset=0;{';'.join(filters) if filters else ''}"
    print(f"\nPerforming {env['url']}/{prefix}/{config_item};{';'.join(filters) if filters else ''}...\n")
    total_count = session.request("GET", total_count_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    # Exception handler
    if 'errors' in total_count:
        raise Exception(f"\n\nError while sending {total_count_request}."
                        f" \nError message: {total_count['errors']['error']}\n")

    # Retrieve total count
    try:
        total_count = total_count['limit'] if total_count['limit'] != 100 else total_count['totalCount']
    except:
        # if we're here -> tags/taxonomies
        total_count = 1

    # Sequentially get all items (batch_size at a time)
    for _ in tqdm(range(0, int(total_count / batch_size) + 1), desc=f"Retrieving {config_item}"):

        try:
            # Get batch of items from API
            batched_item_request = f"{env['url']}/{prefix}/{config_item};offset={str(offset)};{';'.join(filters) if filters else ''}"
            items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

            # Exception handler
            if 'errors' in items_batch:
                raise Exception(f"\n\nError while sending {batched_item_request}. "
                                f"\nError message: {items_batch['errors']['error']}\n")

            # Add batch of items to the list
            items.extend(items_batch[config_item] if config_item in items_batch else items_batch)

            # Incr. offset
            offset = offset + batch_size
        except KeyError as e:
            print(f"Either empty result from API or exact same number for totalCount and batch_size. \n"
                  f"Error is: {e}. Skipping.")

    # Convert list of items to dict
    items_dict = {}
    try:
        for item in items:
            items_dict[f"{item['name']} [{item['id']}]"] = item  # item_name: item_config
    except:
        for item in items:
            items_dict[f"{item['time']} [{item['id']}]"] = item  # event_time: event

    # Sort items dict by name (ignoring case)
    sorted_items_dict = {i: items_dict[i] for i in sorted(list(items_dict.keys()), key=lambda s: s.casefold())}

    # Get all items sub_items from API
    for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} {sub_items}"):
        for sub_item in sub_items:
            sub_item_request = f"{env['url']}/{prefix}/{config_item}/{str(items_dict[item]['id'])}/{sub_item}"
            sorted_items_dict[item][sub_item] = session.request("GET", sub_item_request, headers=HEADERS, auth=auth,
                                                                data=PAYLOAD).json() if sub_item != "body" else \
                session.request("GET", sub_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).content.decode(
                    "utf-8", "ignore").strip()

    return sorted_items_dict
