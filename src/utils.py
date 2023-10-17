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

from src.env import get_env

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def reformat_tabs(match):
    """
    Reformat tabs for groovy scripts.

    :param match:
    :return:
    """

    return match.group(0)[1:]


def reformat_spaces(match):
    """
        Reformat spaces for groovy scripts.

        :param match:
        :return:
        """

    return match.group(0)[4:]


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


def get_items(config_item: str, sub_items: List[str] = [], filters: List[str] = [],
              environment: str = "default") -> dict:
    """
    Get items from an env using public API.

    :param environment: environment to get the items from
    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param sub_items: sub items to retrieve for item_name
    :param filters: filters to apply

    :return: dict['item_name': {item_config}]
    """

    # init. function variables
    offset = 0
    batch_size = 100
    items = []

    # encode fql
    if filters:
        for idx, filter in enumerate(filters):
            if "fql=" in filter:
                filters[idx] = "fql=" + urllib.parse.quote(filter.replace("fql=", ""))

    # retrieve auth material
    env, auth = get_auth_material(environment=environment)

    # get total count
    test_query_result = query(
        method="GET",
        url=f"{config_item}{';' + ';'.join(filters) if filters else ''}",
        environment=environment
    )

    # retrieve totalCount
    total_count = test_query_result['limit'] if test_query_result['limit'] != batch_size else test_query_result[
        'totalCount']

    if total_count != 0:

        # sequentially get all items (batch_size at a time)
        for _ in tqdm(range(0, int(total_count / batch_size) + 1), desc=f"Retrieving {config_item}"):

            # get batch of items from API
            items_batch = query(
                method="GET",
                url=f"{config_item};offset={str(offset)}{';' + ';'.join(filters) if filters else ''}",
                environment=environment,
                log=False
            )

            # add batch of items to the list
            items.extend(items_batch[config_item] if config_item in items_batch else items_batch)

            # incr. offset
            offset = offset + batch_size

        # convert list of items to dict
        items_dict = {}

        # item name formatting in resulting dict
        try:
            if config_item != "collections":
                for item in items:
                    items_dict[f"{item['name']} [{item['id']}]"] = item  # item_name: item_config
            else:
                for item in items:
                    items_dict[f"{item['name']} [{item['uuid']}]"] = item  # collection_name: collection_config
        # exception handler for events
        except Exception as ex:
            for item in items:
                items_dict[f"{item['time']} [{item['id']}]"] = item  # event_time: event

        # sort items dict by name (ignoring case)
        sorted_items_dict = {i: items_dict[i] for i in sorted(list(items_dict.keys()), key=lambda s: s.casefold())}

        # get all items sub_items from API
        for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} {sub_items}"):
            for sub_item in sub_items:

                try: # try bcz some metadata are sometimes empty :)
                    if sub_item != "body":
                        sorted_items_dict[item][sub_item] = query(
                            method="GET",
                            url=f"{config_item}/{str(items_dict[item]['id'] if config_item != 'collections' else str(items_dict.get(item).get('uuid')))}/{sub_item}",
                            environment=environment,
                            log=False
                        )
                    else:
                        sorted_items_dict[item][sub_item] = session.request(
                            "GET",
                            f"{env['url']}/api/{config_item}/{str(items_dict[item]['id'] if config_item != 'collections' else str(items_dict.get(item).get('uuid')))}/{sub_item}",
                            headers=HEADERS,
                            auth=auth,
                            data=PAYLOAD
                        ).content.decode("utf-8", "ignore").strip()
                except:
                    pass

        return sorted_items_dict

    else:

        print(f"No {config_item} found for the given parameters. ")

        return {}


def get_surrounding_items(config_item: str, items: dict, sub_items: List[str]):
    """
    Get surrounding items of a config item.

    :param config_item: config item
    :param items: items to get the sub_items of
    :param sub_items: surrounding items to get
    :return:
    """

    for item in tqdm(items, desc="Retrieving jobs ['asset', 'workflow']"):

        # asset
        try:
            asset_id = items.get(item).get('asset').get('id')
            asset = query(method="GET", url=f"assets/{asset_id};includeMetadata=true", log=False)
            items[item]['asset'] = asset
        except:
            pass

        # workflow
        try:
            workflow_id = items.get(item).get('workflow').get('id')
            workflow_instance = query(method="GET", url=f"workflows/{workflow_id}", log=False)
            workflow_variables = query(method="GET", url=f"workflows/{workflow_id}/variables", log=False)
            items[item]['workflow'] = workflow_instance
            items[item]['workflow']['variables'] = workflow_variables
        except:
            pass

    return items


def get_taxonomies(filters: List[str]):
    """
    Get taxonomies from public API

    :param filters: filters to apply
    :return:
    """

    # encode fql
    if filters:
        for idx, filter in enumerate(filters):
            if "fql=" in filter:
                filters[idx] = "fql=" + urllib.parse.quote(filter.replace("fql=", ""))

    # retrieve default env
    env = get_env()

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # get total count
    taxonomies_request = f"{env['url']}/api/taxonomies{';' + ';'.join(filters) if filters else ''}"
    print(f"\nPerforming [GET] {env['url']}/api/taxonomies{';' + ';'.join(filters) if filters else ''}...")
    taxonomies = session.request("GET", taxonomies_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    enabled_taxonomies = []
    for idx, taxonomy in enumerate(taxonomies):
        if taxonomy['enabled']:
            enabled_taxonomies.append(taxonomies[idx])

    # get taxons
    taxonomies = get_taxons(taxonomies=enabled_taxonomies, env=env, auth=auth)

    return taxonomies


def get_taxons(taxonomies: List[dict], env, auth, url: str = None):
    """
    Get taxonomies' taxons - recursively

    :param taxonomies: taxonomies
    :param env: env
    :param auth: auth
    :param url: url to use
    :return:
    """

    # this one is pretty hard to understand
    for idx, taxonomy in enumerate(taxonomies):

        # build and send api call
        root_taxons_request = f"{env['url']}/api/taxonomies/{taxonomy['id']}/taxons" if not url else url
        taxonomies[idx]['childTaxons'] = session.request("GET", root_taxons_request, headers=HEADERS,
                                                         auth=auth).json()
        try:
            # for root taxons' children (childTaxons)
            for idx2, child_taxon in enumerate(taxonomies[idx]['childTaxons']):
                # only retrieve the enabled ones
                if taxonomies[idx]['childTaxons'][idx2]['enabled']:
                    # check for children recursively if root taxon child has children
                    if taxonomies[idx]['childTaxons'][idx2]['hasChildren']:
                        taxonomies[idx]['childTaxons'][idx2]['childTaxons'] = get_taxons(
                            taxonomies=[taxonomies[idx]['childTaxons'][idx2].copy()],
                            env=env,
                            auth=auth,
                            url=f"{root_taxons_request}/{taxonomies[idx]['childTaxons'][idx2]['id']}/taxons"
                        )[0]['childTaxons']['taxons']
        except:
            # for childTaxons children
            for idx2, child_taxon in enumerate(taxonomies[idx]['childTaxons']['taxons']):
                # only retrieve the enabled ones
                if taxonomies[idx]['childTaxons']['taxons'][idx2]['enabled']:
                    # check for children recursively if taxon has children
                    if taxonomies[idx]['childTaxons']['taxons'][idx2]['hasChildren']:
                        taxonomies[idx]['childTaxons']['taxons'][idx2]['childTaxons'] = get_taxons(
                            taxonomies=[taxonomies[idx]['childTaxons']['taxons'][idx2].copy()],
                            env=env,
                            auth=auth,
                            url=f"{root_taxons_request.split('taxons/')[0]}taxons/{taxonomies[idx]['childTaxons']['taxons'][idx2]['id']}/taxons"
                        )[0]['childTaxons']['taxons']

    return taxonomies


def get_tags_and_taxonomies(metadata_definitions: dict, save_to: str = "",
                            mode: List[str] = ['tagCollections', 'taxonomies']):
    """
    Get taxonomies and tags from metadata def configs.

    :param mode: which items to retrieve
    :param metadata_definitions: dict of metadata defs
    :param save_to: where to save the config
    """

    # init. tax & tags
    taxonomies = []
    tags = []

    # retrieve default env
    env = get_env()

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # fetch tax & tags
    for metadata_definition in metadata_definitions.keys():
        if f"definition" in metadata_definitions[metadata_definition]:
            if f"definition" in metadata_definitions[metadata_definition]["definition"]:
                dig_for_tags_and_taxonomies(
                    entries=metadata_definitions[metadata_definition]["definition"]["definition"],
                    tags=tags,
                    taxonomies=taxonomies
                )

    # fetch tags
    if 'tagCollections' in mode:
        tag_dict = dict()
        for tag in tqdm(set(tags), desc=f"Retrieving tags"):
            # Get tag collections
            tag_request = f"{env['url']}/api/tagCollections/{tag}"
            tag_collection = session.request("GET", tag_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()
            tag_dict[tag_collection['displayName']] = tag_collection

        # sort
        sorted_tag_dict = {i: tag_dict[i] for i in sorted(list(tag_dict.keys()))}

    # fetch taxonomies
    if 'taxonomies' in mode:
        tax_dict = dict()
        for tax in tqdm(set(taxonomies), desc=f"Retrieving taxonomies"):
            # get taxonomies
            tax_request = f"{env['url']}/api/taxonomies/{tax}"
            taxonomy = session.request("GET", tax_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()
            try:
                tax_dict[taxonomy['displayName']] = taxonomy
            except:
                continue

        # sort
        sorted_tax_dict = {i: tax_dict[i] for i in sorted(list(tax_dict.keys()))}

    # save tags as JSON
    if save_to and 'tagCollections' in mode:
        with open(f"{save_to}/configs/tags.json", "w") as tags_config:
            json.dump(obj=sorted_tag_dict, fp=tags_config, indent=4)
            print(f"tags have been saved to {save_to}/configs/tags.json")

    # save taxonomies as JSON
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

    # recursively search for tags and taxonomies
    for entry in entries:
        if "backingStoreType" in entry:
            # tags
            if entry['backingStoreType'] == "USER_DEFINED_TAG_COLLECTION" and "backingStoreInstanceId" in entry:
                tags.append(entry['backingStoreInstanceId'])
            # taxonomies
            elif entry['backingStoreType'] == "TAXONOMY" and "filter" in entry:
                taxonomies.append(entry['filter'])

        # recursive
        elif "children" in entry:
            dig_for_tags_and_taxonomies(entries=entry["children"], tags=tags, taxonomies=taxonomies)


def get_auth_material(environment: str = "default"):
    """
    Returns auth material: env & auth.

    :return:
    """

    # retrieve default env
    env = get_env(environment=environment)

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    return env, auth


def query(method: str, url: str, payload=None, log: bool = True, environment: str = "default"):
    """
    Query the public API.

    :param environment: env to query
    :param method: method to use from [GET, POST, PUT]
    :param url: url to query after env_url/api/
    :param payload: payload to use for POST & PUT queries
    :param log: whetherto log performed action in terminal or not

    :return:
    """

    # auth material
    env, auth = get_auth_material(environment=environment)

    # query
    query = f"{env['url']}/api/{url}" if "http" not in url else f"{url}"

    if log:
        print(f"\nPerforming [{method}] {query}...\n")

    query_result = session.request(
        method,
        query,
        headers=HEADERS,
        auth=auth,
        data=json.dumps(payload) if payload else None
    ).json()

    # exception handler
    if 'errors' in query_result:
        raise Exception(f"\n\nError while sending {query}. \nError message: {query_result['errors']['error']}\n ")

    return query_result
