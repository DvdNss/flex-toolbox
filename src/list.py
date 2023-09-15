"""

    PROJECT: flex_toolbox
    FILENAME: list.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""

import requests
from requests.auth import HTTPBasicAuth

from src.env import get_default_env

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. session
session = requests.Session()


def list_command_func(args):
    """Action on list command. """

    list_items(name=args.config_item, contains=args.contains)


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
        total_count_request = f"{env['url']}/api/{name};limit=1;offset=0;name=end"
        total_count = session.request("GET", total_count_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()[
            'totalCount']
    except Exception as ex:
        print(f"ERROR: {ex}")
        return False

    # Sequentially get all items (batch_size at a time)
    for _ in range(0, int(total_count / batch_size) + 1):

        try:
            # Get batch of items from API
            batched_item_request = f"{env['url']}/api/{name};limit={str(batch_size)};offset={str(offset)};name=end"
            items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth,
                                          data=PAYLOAD).json()

            # Add batch of items to the list
            items.extend(items_batch[name])

            # Incr. offset
            offset = offset + batch_size
        except KeyError as e:
            print(f"ERROR: {e}")
            return False

    # Sort the list
    sorted_items = sorted(items, key=lambda x: x['name'].lower())

    # Convert list of items to dict
    for item in sorted_items:
        print(f"[{item['name']}] - ID: {item['id']}") if contains in item['name'].lower() else None

    return True
