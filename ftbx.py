#!/usr/bin/python

"""

    PROJECT: flex_toolbox
    FILENAME: toolbox.py
    AUTHOR: David NAISSE
    DATE: September 07, 2023

    DESCRIPTION: TODO
    
"""

import argparse
import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth
from rich.console import Console

from VARIABLES import ACTION_CONFIG, WORKFLOW_CONFIG, DEFAULT_GROOVY_SCRIPT, FLEX_CONFIG_ITEMS

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. logger
logger = logging.getLogger(__name__)

# Init. console
console = Console()

# Init. session
session = requests.Session()


def log(msg: str, level: str = "info", style: str = "", in_console: bool = True) -> None:
    """
    Log a message in both the console and the logger.

    :param msg: message
    :param level: log level
    :param style: color to show in console
    :param in_console: whether to log the msg in console or not
    """

    if "i" in level:
        msg = "INFO: " + msg
    elif "w" in level:
        msg = "WARN: " + msg
    elif "e" in level:
        msg = "ERROR: " + msg
        style = "bold red"

    if in_console:
        console.print(msg, style=style)


def read_environments_json():
    """
    Read or creates the environments.json file.

    :return:
    """

    try:
        # Read existing json
        with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "r") as file:
            environments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with the default content
        environments = {}
        with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "w") as file:
            json.dump(environments, file, indent=4)

    return environments


def get_default_env():
    """
    Return default environment.

    :return:
    """

    environments = read_environments_json()

    return environments['environments']['default']


def ping(env: str, username: str, password: str):
    """
    Ping Flex env with credentials.

    :param env: env url
    :param username: username
    :param password: password
    :return:
    """

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=username, password=password)

    # Send a test request
    response = session.request("GET", f"{env}/api/accounts;limit=1", headers=HEADERS, auth=auth, data=PAYLOAD).json()

    # Handle connection unavailable
    if "errors" in response:
        log(msg=f"ERROR {response['errors']['error']}", level="e", style="bold red")
        raise Exception(response["errors"]["error"])
    else:
        log(msg=f"Successfully connected to {env} - this environment is now your default environment.", in_console=True)


def add_or_update_environments_json(env, username, password, isDefault: bool = False):
    """
    Add env to enrionments.json

    :param env: env url
    :param username: username
    :param password: password
    :param isDefault: whether the env is default or not
    :return:
    """

    # Read
    with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "r") as environments_file:
        environments = json.load(environments_file)

    # Update
    environments['environments'][env if not isDefault else "default"] = {
        "url": env,
        "username": username,
        "password": password,
    }

    # Save
    with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "w") as environments_file:
        json.dump(environments, environments_file, indent=4)

    return environments['environments'][env if not isDefault else "default"]


def connect(url_or_alias: str, username: str = None, password: str = None):
    """
    Connects to a Flex env with url or alias only by ready environments.json

    :param url_or_alias: url or alias of the env
    :param username: username (optional)
    :param password: password (optional)
    :return:
    """

    environments = read_environments_json()
    env = None

    # Retrieve env by alias
    try:
        for e in environments['environments']:
            if url_or_alias in e:
                env = environments['environments'][e]
        if env is None: raise Exception
    # If it fails, retrieve env by url
    except:
        for e in environments['environments']:
            if url_or_alias in environments['environments'][e]['url']:
                env = environments['environments'][e]

    # If env is not registered and no username/password provided
    if not env and not password and not username:
        log(msg="Unable to recognize environment, please check the information is correct or provide username and password. ",
            in_console=True, style="bold red")
        return None
    # If env not registered but username and password provided
    elif not env and password and username:
        env = add_or_update_environments_json(env=url_or_alias, username=username, password=password)

    # Test connection and default if successful
    ping(env=env['url'], username=env['username'], password=env['password'])
    add_or_update_environments_json(env=env['url'], username=env['username'], password=env['password'], isDefault=True)

    return env


def create_folder(folder_name: str):
    """
    Create folder or return error if already exists.

    :param folder_name: folder name
    :return: True if created, False if error
    """

    try:
        os.mkdir(folder_name)
        log(msg="Folder " + folder_name + " was created. ", level="i")
        return True
    except FileExistsError:
        log(msg="Folder " + folder_name + " already exists. ", level="e", style="bold red")
        return False


def create_object(name: str, type: str):
    """
    Create config

    :param name: object name
    :param type: type from [action, workflow]
    :return: True if created, False if failed
    """

    with open(name + "/config.json", "w") as config_file:
        if type == "action":
            # Creates config.json file
            config = ACTION_CONFIG
            config['name'] = name
            config['pluginClass'] = "tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand"
            config['accountId'] = get_default_account_id()
            config['visibilityIds'] = [get_default_account_id()]
            config['pluginUuid'] = "cab6f437-3ce0-4857-9578-fd519b783d66"
            json.dump(ACTION_CONFIG, config_file, indent=4)
            # Creates script.groovy file
            with open(name + "/script.groovy", "w") as groovy_file:
                groovy_file.write(DEFAULT_GROOVY_SCRIPT)
        elif type == "workflow":
            json.dump(WORKFLOW_CONFIG, config_file, indent=4)
        else:
            log(msg="Cannot recognize object type. Aborting...", level="e", style="bold red")
            return False

    log(msg=name + "/config.json with " + type + " config has been created.", level="i")
    return True


def get_default_account_id():
    """
    Retrieve account id for the default env.

    :return:
    """

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # Get default account id
    try:
        accounts_query = f"{env['url']}/api/accounts;limit=1;offset=0"
        accounts = session.request("GET", accounts_query, headers=HEADERS, auth=auth, data=PAYLOAD).json()['accounts']
        account = accounts[0]['id']

        return account
    except:
        log(msg="Failed to retrieve default account.", level="e")
        return 0


def list_items(name: str, contains: str = "") -> bool:
    """
    List items ids.

    :param name: item to retrieve from API (ex: workflows, accounts..)
    :param contains: contains a specific string

    :return: True if succeeds, False if fails
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
    try:
        total_count_request = f"{env['url']}/api/{name};limit=1;offset=0"
        total_count = session.request("GET", total_count_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()[
            'totalCount']
    except:
        log(msg="Failed to retrieve items for " + name + ".", level="e")
        return False

    # Sequentially get all items (batch_size at a time)
    for _ in range(0, int(total_count / batch_size) + 1):

        try:
            # Get batch of items from API
            batched_item_request = f"{env['url']}/api/{name};limit={str(batch_size)};offset={str(offset)}"
            items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

            # Add batch of items to the list
            items.extend(items_batch[name])

            # Incr. offset
            offset = offset + batch_size
        except KeyError as e:
            print(
                f"Either empty result from API or exact same number for totalCount and batch_size. Error is: {e}. Skipping.")
            return False

    # Sort the list
    sorted_items = sorted(items, key=lambda x: x['name'].lower())

    # Convert list of items to dict
    for item in sorted_items:
        print(f"[{item['name']}] - ID: {item['id']}") if contains in item['name'].lower() else None

    return True


if __name__ == "__main__":

    # Script args
    parser = argparse.ArgumentParser(description='Flex ToolBox')
    parser.add_argument('tool', type=str, help='Flex tool to use.')
    parser.add_argument('options', type=str, nargs='*', help='Tool options')
    parser.add_argument('--contains', type=str, help="Name to search", default="")
    args = parser.parse_args()

    # Connect to an environment
    if args.tool == "connect":
        # connect with alias or url without creds
        if len(args.options) == 1:
            env = connect(url_or_alias=args.options[0])
            if not env:
                quit()
        # connect to url with creds
        elif len(args.options) == 3:
            env = connect(url_or_alias=args.options[0], username=args.options[1], password=args.options[2])
            if not env:
                quit()
    # Show current environment
    elif args.tool == "env":
        # Log default environment
        default_env = read_environments_json()['environments']['default']
        log(msg=f"Current default environment is {default_env['url']} - user: {default_env['username']}. ",
            in_console=True)
    # Create action
    elif args.tool == "create_action":
        # create a single action
        if len(args.options) == 1:
            quit() if not create_folder(folder_name=args.options[0]) else None
            quit() if not create_object(name=args.options[0], type="action") else None
        # invalid scenario
        else:
            log(msg="No action or too many actions given as parameters. ", level="e", style="bold red")
    # Create workflow
    elif args.tool == "create_workflow":
        # create a single action
        if len(args.options) == 1:
            quit() if not create_folder(args.options[0]) else None
        # invalid scenario
        else:
            log(msg="No workflow or too many workflow given as parameters. ", level="e", style="bold red")
    # List config items
    elif args.tool == "list":
        # for config objects
        if len(args.options) == 1 and args.options[0] in FLEX_CONFIG_ITEMS:
            quit() if not list_items(name=args.options[0], contains=args.contains) else None
        # invalid scenario
        else:
            log(msg="No object, too many objects, or incorrect object given as parameters. ", level="e", style="bold red")
    # Pull config items
    elif args.tool == "pull":
        # TODO: pull actions etc with 'all' option
        print("TODO")