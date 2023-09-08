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

import requests
from requests.auth import HTTPBasicAuth
from rich.console import Console

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
        logger.info(msg=msg)
    elif "w" in level:
        logger.warning(msg=msg)
    elif "e" in level:
        logger.error(msg=msg)

    if in_console:
        console.print(msg, style=style)


def read_environments_json():
    """
    Read or creates the environments.json file.

    :return:
    """

    try:
        # Read existing json
        with open("environments.json", "r") as file:
            environments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with the default content
        environments = {}
        with open("environments.json", "w") as file:
            json.dump(environments, file, indent=4)

    return environments


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
    with open("environments.json", "r") as environments_file:
        environments = json.load(environments_file)

    # Update
    environments['environments'][env if not isDefault else "default"] = {
        "url": env,
        "username": username,
        "password": password,
    }

    # Save
    with open("environments.json", "w") as environments_file:
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


if __name__ == "__main__":

    # Script args
    parser = argparse.ArgumentParser(description='Flex ToolBox')
    parser.add_argument('tool', type=str, help='Flex tool to use.')
    parser.add_argument('options', type=str, nargs='*', help='Tool options')
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

    elif args.tool == "env":

        # Log default environment
        default_env = read_environments_json()['environments']['default']
        log(msg=f"Current default environment is {default_env['url']} - user: {default_env['username']}. ", in_console=True)
