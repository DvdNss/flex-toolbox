"""

    PROJECT: flex_toolbox
    FILENAME: list.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import urllib.parse
from typing import List

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

    list_items(config_item=args.config_item, filters=args.filters)

    # TODO: custom for userDefinedObject, tagCollections


def list_items(config_item: str, filters: List[str] = []) -> bool:
    """
    List items ids.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param filters: filters to apply

    :return: True if succeeds, False if fails
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

    total_count_request = f"{env['url']}/api/{config_item};offset=0;{';'.join(filters) if filters else ''}"
    total_count = session.request("GET", total_count_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()
    print(f"\nPerforming [GET] {env['url']}/api/{config_item};{';'.join(filters) if filters else ''}...\n")

    if 'errors' in total_count:
        raise Exception(
            f"\n\nError while sending {total_count_request}. \nError message: {total_count['errors']['error']}\n")

    total_count = total_count['totalCount']

    # Sequentially get all items (batch_size at a time)
    for _ in range(0, int(total_count / batch_size) + 1):

        # Get batch of items from API
        batched_item_request = f"{env['url']}/api/{config_item};offset={str(offset)};{';'.join(filters) if filters else ''}"
        items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

        if 'errors' in items_batch:
            raise Exception(
                f"\n\nError while sending {batched_item_request}. \nError message: {items_batch['errors']['error']}\n")

        # Add batch of items to the list
        items.extend(items_batch[config_item])

        # Incr. offset
        offset = offset + batch_size

    # Sort the list
    sorted_items = sorted(items, key=lambda x: x['name'].lower())

    # Convert list of items to dict
    if sorted_items:
        for item in sorted_items:
            print(f"[{item['name']}] - ID: {item['id']}")
    else:
        print(f"No {config_item} found for the given parameters. ")
    print("")

    return True
