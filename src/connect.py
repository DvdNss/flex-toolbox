"""

    PROJECT: flex_toolbox
    FILENAME: connect.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: connect command
    
"""

import requests
from requests.auth import HTTPBasicAuth

from src.env import read_environments_json, add_or_update_environments_json, get_default_env

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def connect_command_func(args):
    """Action on connect command. """

    connect(url_or_alias=args.env_url, username=args.username, password=args.password)


def ping(env: str, username: str, password: str):
    """
    Ping Flex env with credentials.

    :param env: env url
    :param username: username
    :param password: password
    :return:
    """

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=username, password=password)

    # send a test request
    response = session.request("GET", f"{env}/api/accounts;limit=1", headers=HEADERS, auth=auth, data=PAYLOAD).json()

    # handle connection unavailable
    if "errors" in response:
        print(f"ERROR: {response['errors']['error']}")
        raise Exception(response["errors"]["error"])
    else:
        print(f"Successfully connected to {env} - this environment is now your default environment.")


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

    # retrieve env by alias
    try:
        for e in environments['environments']:
            if url_or_alias in e:
                env = environments['environments'][e]
        if env is None: raise Exception
    # if it fails, retrieve env by url
    except:
        for e in environments['environments']:
            if url_or_alias in environments['environments'][e]['url']:
                env = environments['environments'][e]

    # if env is not registered and no username/password provided
    if not env and not password and not username:
        print(f"Unable to recognize environment, please check the information is correct or provide username/password.")
        return False
    # if env not registered but username and password provided
    elif not env and password and username:
        env = add_or_update_environments_json(env=url_or_alias, username=username, password=password)

    # test connection and default if successful
    ping(env=env['url'], username=env['username'], password=env['password'])
    add_or_update_environments_json(env=env['url'], username=env['username'], password=env['password'], isDefault=True)

    return True


def get_default_account_id():
    """
    Retrieve account id for the default env.

    :return:
    """

    # retrieve default env
    env = get_default_env()

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # get default account id
    try:
        accounts_query = f"{env['url']}/api/accounts;limit=1;offset=0"
        accounts = session.request("GET", accounts_query, headers=HEADERS, auth=auth, data=PAYLOAD).json()['accounts']
        account = accounts[0]['id']

        return account
    except:
        print(f"Failed to retrieve default account.")
        return 0
