"""

    PROJECT: flex_toolbox
    FILENAME: connect.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: connect command
    
"""

import requests
from requests.auth import HTTPBasicAuth

from src.env import read_environments_json, add_or_update_environments_json, get_env
from src.utils import query

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def connect_command_func(args):
    """Action on connect command. """

    connect(url_or_alias=args.env_url, username=args.username, password=args.password)


def ping(env: str, username: str, password: str, log: bool = True):
    """
    Ping Flex env with credentials.

    :param env: env url
    :param username: username
    :param password: password
    :param log: whether to log
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
        print(f"Successfully connected to {env} - this environment is now your default environment.") if log else None


def connect(url_or_alias: str, username: str = None, password: str = None, log: bool = True):
    """
    Connects to a Flex env with url or alias only by reading environments.json

    :param url_or_alias: url or alias of the env (can be a shortened version)
    :param username: username (optional)
    :param password: password (optional)
    :param log: whether to log
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
        print(f"Unable to recognize environment {env}, please check the information and username/password are correct.")
        return False
    # if env not registered but username and password provided
    elif not env and password and username:
        env = add_or_update_environments_json(env=url_or_alias, username=username, password=password)

    # test connection and default if successful
    ping(env=env['url'], username=env['username'], password=env['password'], log=log)
    add_or_update_environments_json(env=env['url'], username=env['username'], password=env['password'], is_default=True)

    return True


def get_default_account_id(environment: str = "default"):
    """
    Retrieve account id for the default env.

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
