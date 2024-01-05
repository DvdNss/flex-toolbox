"""

    PROJECT: flex_toolbox
    FILENAME: connect.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: connect command

    TEST STATUS: FULLY TESTED
"""
import time

import requests
from requests.auth import HTTPBasicAuth

from src.encryption import decrypt_pwd
from src.env import read_environments_json, add_or_update_environments_json
from src.utils import query

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def connect_command_func(args):
    """
    Action on connect command.

    TEST STATUS: FULLY TESTED
    """

    connect(url_or_alias=args.env_url, username=args.username, password=args.password, alias=args.alias)


def connect(url_or_alias: str, username: str = None, password: str = None, alias: str = None, log: bool = True):
    """
    Connects to a Flex env with url or alias only by reading environments.json

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param url_or_alias: url or alias of the env (can be a shortened version)
    :param username: username (optional)
    :param password: password (optional)
    :param alias: alias to use for env creation
    :param log: whether to log
    :return:
    """

    environments = read_environments_json()
    existing_env = None
    existing_alias = None

    # check if env exists
    for e in environments['environments']:
        if url_or_alias == e or url_or_alias == environments['environments'][e]['url'] and e != "default":
            existing_env = environments['environments'][e]
            existing_alias = e

    url = url_or_alias if not existing_env else existing_env.get('url')
    alias = existing_alias if existing_alias else alias

    # ping
    try:
        start_time = time.time()
        response = session.request(
            method='GET',
            url=f"{url}/api/resources;limit=1",
            auth=HTTPBasicAuth(
                username=username if username else existing_env.get('username'),
                password=password if password else decrypt_pwd(existing_env.get('password'))),
            timeout=(1, 1),
        ).json()
    except AttributeError as ae:
        raise Exception(f"\n\nError: [{url_or_alias}] does not exist. Please check the information provided. \n ")

    if 'errors' in response:
        raise Exception(f"\n\nError: {str(response['errors'])}\n ")
    else:
        end_time = time.time()
        print(f"\nSTATUS: Connection successful ({round(end_time - start_time, 3)} seconds)") if log else None

    if username and password:
        # add or update
        existing_env = add_or_update_environments_json(
            env=url,
            username=username,
            password=password,
            alias=alias
        )

    # set default
    default_env = add_or_update_environments_json(
        env=existing_env.get('url'),
        username=existing_env.get('username'),
        password=existing_env.get('password'),
        alias=alias,
        is_default=True
    )
    print(f"\nDEFAULT ENVIRONMENT: {default_env.get('url')} [{alias}] as {default_env.get('username')}\n") if log else None

    return True


def get_default_account_id(environment: str = "default"):
    """
    Retrieve account id for the default env.

    TEST STATUS: FULLY TESTED

    :return:
    """

    # get default account id
    try:
        accounts = query(method="GET", url="accounts;limit=1", log=False, environment=environment)['accounts']
        account_id = accounts[0]['id']

        return account_id
    except:
        print(f"Failed to retrieve default account.")
        return 0
