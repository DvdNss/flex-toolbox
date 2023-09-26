"""

    PROJECT: flex_toolbox
    FILENAME: utils.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: functions that are used across the project
    
"""
import json
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
    test_request = f"{env['url']}/{prefix}/{config_item};offset=0;{';'.join(filters) if filters else ''}"
    print(f"\nPerforming [GET] {env['url']}/{prefix}/{config_item}{';' + ';'.join(filters) if filters else ''}...\n")
    test_response = session.request("GET", test_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    # Exception handler
    if 'errors' in test_response:
        raise Exception(f"\n\nError while sending {test_request}."
                        f" \nError message: {test_response['errors']['error']}\n")

    # Retrieve totalCount
    total_count = test_response['limit'] if test_response['limit'] != 100 else test_response['totalCount']

    # Sequentially get all items (batch_size at a time)
    for _ in tqdm(range(0, int(total_count / batch_size) + 1), desc=f"Retrieving {config_item}"):

        try:
            batched_item_request = f"{env['url']}/{prefix}/{config_item};offset={str(offset)};{';'.join(filters) if filters else ''}"

            # Get batch of items from API
            items_batch = session.request("GET", batched_item_request, headers=HEADERS, auth=auth,
                                          data=PAYLOAD).json()

            # Exception handler
            if 'errors' in items_batch:
                raise Exception(f"\n\nError while sending {batched_item_request}. "
                                f"\nError message: {items_batch['errors']['error']}\n")

            # Add batch of items to the list
            items.extend(items_batch[config_item] if config_item in items_batch else items_batch)

            # Incr. offset
            offset = offset + batch_size

        # Exception handler
        except KeyError as e:
            print(f"Either empty result from API or exact same number for totalCount and batch_size. \n"
                  f"Error is: {e}. Skipping.")

    # Convert list of items to dict
    items_dict = {}

    try:
        if config_item != "collections":
            for item in items:
                items_dict[f"{item['name']} [{item['id']}]"] = item  # item_name: item_config
        else:
            for item in items:
                items_dict[f"{item['name']} [{item['uuid']}]"] = item  # collection_name: collection_config
    # Exception handler for events
    except Exception as ex:
        for item in items:
            items_dict[f"{item['time']} [{item['id']}]"] = item  # event_time: event

    # Sort items dict by name (ignoring case)
    sorted_items_dict = {i: items_dict[i] for i in sorted(list(items_dict.keys()), key=lambda s: s.casefold())}

    # Get all items sub_items from API
    for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} {sub_items}"):
        for sub_item in sub_items:
            sub_item_request = f"{env['url']}/{prefix}/{config_item}/{str(items_dict[item]['id'] if config_item is not 'collections' else str(items_dict.get(item).get('uuid')))}/{sub_item}"
            sorted_items_dict[item][sub_item] = session.request("GET", sub_item_request, headers=HEADERS, auth=auth,
                                                                data=PAYLOAD).json() if sub_item != "body" else \
                session.request("GET", sub_item_request, headers=HEADERS, auth=auth, data=PAYLOAD).content.decode(
                    "utf-8", "ignore").strip()

    return sorted_items_dict


def get_tags_and_taxonomies(metadata_definitions: dict, save_to: str = "",
                            mode: List[str] = ['tagCollections', 'taxonomies']):
    """
    Get taxonomies and tags from metadata def configs.

    :param mode: which items to retrieve
    :param metadata_definitions: dict of metadata defs
    :param save_to: where to save the config
    """

    # Init. tax & tags
    taxonomies = []
    tags = []

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # Fetch tax & tags
    for metadata_definition in metadata_definitions.keys():
        if f"definition" in metadata_definitions[metadata_definition]:
            if f"definition" in metadata_definitions[metadata_definition]["definition"]:
                dig_for_tags_and_taxonomies(
                    entries=metadata_definitions[metadata_definition]["definition"]["definition"],
                    tags=tags,
                    taxonomies=taxonomies
                )

    # Fetch tags
    if 'tagCollections' in mode:
        tag_dict = dict()
        for tag in tqdm(set(tags), desc=f"Retrieving tags"):
            # Get tag collections
            tag_request = f"{env['url']}/api/tagCollections/{tag}"
            tag_collection = session.request("GET", tag_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()
            tag_dict[tag_collection['displayName']] = tag_collection

        # Sort
        sorted_tag_dict = {i: tag_dict[i] for i in sorted(list(tag_dict.keys()))}

    # Fetch taxonomies
    if 'taxonomies' in mode:
        tax_dict = dict()
        for tax in tqdm(set(taxonomies), desc=f"Retrieving taxonomies"):
            # Get taxonomies
            tax_request = f"{env['url']}/api/taxonomies/{tax}"
            taxonomy = session.request("GET", tax_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()
            try:
                tax_dict[taxonomy['displayName']] = taxonomy
            except:
                continue

        # Sort
        sorted_tax_dict = {i: tax_dict[i] for i in sorted(list(tax_dict.keys()))}

    # Save tags as JSON
    if save_to and 'tagCollections' in mode:
        with open(f"{save_to}/configs/tags.json", "w") as tags_config:
            json.dump(obj=sorted_tag_dict, fp=tags_config, indent=4)
            print(f"tags have been saved to {save_to}/configs/tags.json")

    # Save taxonomies as JSON
    if save_to and 'taxonomies' in mode:
        with open(f"{save_to}/configs/taxonomies.json", "w") as taxonomies_config:
            json.dump(obj=sorted_tax_dict, fp=taxonomies_config, indent=4)
            print(f"taxonomies have been saved to {save_to}/configs/taxonomies.json. ")

    print("")

    if 'tagCollections' in mode and 'taxonomies' not in mode:
        return sorted_tag_dict
    elif 'taxonomies' in mode and 'tagCollections' not in mode:
        return sorted_tax_dict
    else:
        return sorted_tag_dict, sorted_tax_dict


def dig_for_tags_and_taxonomies(entries, tags: List, taxonomies: List):
    """
    Dig deeper to find tags and taxonomies.

    :param entries: entries to search in
    :param tags: list of tags
    :param taxonomies: list of taxonomies
    """

    # Recursively search for tags and taxonomies
    for entry in entries:
        if "backingStoreType" in entry:
            # Tags
            if entry['backingStoreType'] == "USER_DEFINED_TAG_COLLECTION" and "backingStoreInstanceId" in entry:
                tags.append(entry['backingStoreInstanceId'])
            # Taxonomies
            elif entry['backingStoreType'] == "TAXONOMY" and "filter" in entry:
                taxonomies.append(entry['filter'])

        elif "children" in entry:

            dig_for_tags_and_taxonomies(entries=entry["children"], tags=tags, taxonomies=taxonomies)
