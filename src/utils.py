"""

    PROJECT: flex_toolbox
    FILENAME: utils.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: functions that are used across the project

    TEST STATUS: FULLY TESTED
"""
import datetime
import json
import os
import re
import urllib.parse
from typing import List, Union

import graphviz
import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

import VARIABLES
from src.encryption import decrypt_pwd
from src.env import get_env, get_default_env_alias

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def apply_post_retrieval_filters(items, filters, log: bool = True):
    """
    Apply post-API-retrieval filters to some config items.

    TEST STATUS: FULLY TESTED

    :param filters: custom post-processing filters
    :param items: config items dict
    :param log: log or not

    :return:
    """

    # post-filters processing
    for post_filter in tqdm(filters, desc=f"Applying post filters {filters}", disable=not log):
        # operator
        operator = None
        for op in ['!~', '!=', '>=', '<=', '~', '=', '<', '>']:
            if op in post_filter:
                operator = op
                break

        if not operator:
            print(f"Couldn't find operator for [{post_filter}], skipping...")
        else:
            key, value = post_filter.split(operator)
            key = key
            value = value

            filtered_items = {}
            for item in items:

                # get nested value
                item_value = get_nested_value(items[item], key)

                if isinstance(item_value, bool):
                    value = str_to_bool(str(value))
                elif isinstance(item_value, int):
                    value = int(value)
                # todo: handle dates
                # elif isinstance(item_value, str):
                #     try:
                #         value: datetime = datetime.datetime.strptime(value, '%d %b %Y %H:%M:%S %z')
                #         print(value, type(value))
                #         item_value: datetime = datetime.datetime.strptime(item_value, '%d %b %Y %H:%M:%S %z')
                #         print(item_value, type(item_value))
                #     except:
                #         pass

                # switch
                if operator == '=':
                    if item_value == value:
                        filtered_items[item] = items[item]
                elif operator == '!=':
                    if item_value != value:
                        filtered_items[item] = items[item]
                elif operator == '>=':
                    if item_value >= value:
                        filtered_items[item] = items[item]
                elif operator == '<=':
                    if item_value <= value:
                        filtered_items[item] = items[item]
                elif operator == '<':
                    if item_value < value:
                        filtered_items[item] = items[item]
                elif operator == '>':
                    if item_value > value:
                        filtered_items[item] = items[item]
                elif operator == '!~':
                    if isinstance(item_value, str) and value not in item_value:
                        filtered_items[item] = items[item]
                elif operator == '~':
                    if isinstance(item_value, str) and value in item_value:
                        filtered_items[item] = items[item]

            # Replace sorted_items with filtered_items for the next post_filter
            items = filtered_items

    return items


def reformat_tabs(match):
    """
    Reformat tabs for groovy scripts by removing one \t out of many.

    TEST STATUS: FULLY TESTED

    :param match:
    :return:
    """

    return match.group(0)[1:]


def reformat_spaces(match):
    """
    Reformat spaces for groovy scripts by removing one "    " out of many.

    TEST STATUS: FULLY TESTED

    :param match:
    :return:
    """

    return match.group(0)[4:]


def create_folder(folder_name: str, ignore_error: bool = False):
    """
    Create folder or return error if already exists.

    TEST STATUS: FULLY TESTED

    :param folder_name: folder name
    :param ignore_error: whether to ignore folder already exists or not

    :return: True if created, False if error
    """

    try:
        os.mkdir(folder_name)
        return True
    except FileExistsError:
        if ignore_error:
            return True
        else:
            print(f"Folder {folder_name} already exists. ")
            return False


def get_items(config_item: str, sub_items: List[str] = [], filters: List[str] = [],
              environment: str = "default", id_in_keys: bool = True, with_dependencies: bool = False,
              log: bool = True) -> dict:
    """
    Get items from an env using public API.

    TEST STATUS: FULLY TESTED

    :param log: whether to log
    :param environment: environment to get the items from
    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param sub_items: sub items to retrieve for item_name
    :param filters: filters to apply
    :param id_in_keys: whether to put ID in resulting dict keys
    :param with_dependencies: whether to also retrieve item's dependencies

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
    limit = batch_size
    if filters and any("limit" in filter for filter in filters):
        limit = int([filter for filter in filters if "limit" in filter][0].split("=")[1])
    tmp_filters = [filter for filter in filters if f"limit={str(limit)}" not in filter] if filters else []
    tmp_filters.append('limit=1')
    test_query_result = query(
        method="GET",
        url=f"{config_item}{';' + ';'.join(tmp_filters) if tmp_filters else ''}",
        environment=environment,
        log=log
    )

    # retrieve totalCount
    total_count = limit if limit != batch_size else test_query_result['totalCount']

    if total_count != 0:

        # sequentially get all items (batch_size at a time)
        for _ in tqdm(range(0, int(total_count / batch_size) + 1), desc=f"Retrieving {total_count} {config_item}",
                      disable=not log):
            try:
                # get batch of items from API
                items_batch = query(
                    method="GET",
                    url=f"{config_item};offset={str(offset)}{';' + ';'.join(filters) if filters else ''}",
                    environment=environment,
                    log=False
                )

                # add batch of items to the list
                items.extend(items_batch[config_item] if config_item in items_batch else items_batch)
            except AttributeError:
                print(f"API error for batch_size={batch_size} and offset={offset}, skipping...")

            # incr. offset
            offset = offset + batch_size

        # convert list of items to dict
        items_dict = {}

        # item name formatting in resulting dict
        try:
            if config_item != "collections":
                if id_in_keys:
                    for item in items:
                        items_dict[f"{item['name']} [{item['id']}]"] = item  # item_name: item_config
                else:
                    for item in items:
                        items_dict[f"{item['name']}"] = item
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
        for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} {sub_items}", disable=not log):
            for sub_item in sub_items:

                try:  # try bcz some metadata are sometimes empty :)
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

        # find dependencies if config
        if with_dependencies and any(dep_root in sub_items for dep_root in ['configuration', 'structure']):
            for item in tqdm(sorted_items_dict, desc=f"Retrieving {config_item} dependencies", disable=not log):

                if config_item == 'workflowDefinitions':
                    find_and_pull_dependencies(json_config=sorted_items_dict[item]['structure'])
                else:
                    find_and_pull_dependencies(json_config=sorted_items_dict[item]['configuration']['instance'])

        return sorted_items_dict

    else:

        print(f"No {config_item} found for the given parameters. ") if log else None

        return {}


def retry_config_item_instance(config_item: str, id: str, environment: str = "default"):
    """
    Retry config item instance given its id.

    TEST STATUS: FULLY TESTED

    :param config_item: config item
    :param id: object id
    :param environment: environment to retry from
    """

    # payload
    payload = {
        "action": "retry"
    }

    # retry
    query_result = query(
        method="POST",
        url=f"{config_item}/{id}/actions",
        environment=environment,
        payload=payload,
        log=False,
    )

    return query_result.get('name'), query_result.get('progress')


def launch_config_item_instance(config_item: str, payload: dict, environment: str = "default"):
    """
    Launch config item instance.

    TEST STATUS: FULLY TESTED

    :param config_item: config item
    :param payload: payload containing launch parameters
    :param environment: environment to launch in
    :return:
    """

    # retry
    query_result = query(
        method="POST",
        url=f"{config_item}",
        environment=environment,
        payload=payload,
        log=True,
    )

    return query_result


def enumerate_sub_items(config_item: str):
    """
    Returns the list of sub items for a given config item.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param config_item: config item
    :return:
    """

    if config_item == 'accounts':
        return VARIABLES.ACCOUNTS_SUB_ITEMS
    elif config_item == 'actions':
        return VARIABLES.ACTIONS_SUB_ITEMS
    elif config_item == 'assets':
        return VARIABLES.ASSETS_SUB_ITEMS
    elif config_item == 'collections':
        return VARIABLES.COLLECTIONS_SUB_ITEMS
    elif config_item == 'eventHandlers':
        return VARIABLES.EVENT_HANDLERS_SUB_ITEMS
    elif config_item == 'events':
        return VARIABLES.EVENTS_SUB_ITEMS
    elif config_item == 'groups':
        return VARIABLES.GROUPS_SUB_ITEMS
    elif config_item == 'jobs':
        return VARIABLES.JOBS_SUB_ITEMS
    elif config_item == 'messageTemplates':
        return VARIABLES.MESSAGE_TEMPLATES_SUB_ITEMS
    elif config_item == 'metadataDefinitions':
        return VARIABLES.METADATA_DEFINITIONS_SUB_ITEMS
    elif config_item == 'objectTypes':
        return VARIABLES.OBJECT_TYPES_SUB_ITEMS
    elif config_item == 'profiles':
        return VARIABLES.PROFILES_SUB_ITEMS
    elif config_item == 'quotas':
        return VARIABLES.QUOTAS_SUB_ITEMS
    elif config_item == 'resources':
        return VARIABLES.RESOURCES_SUB_ITEMS
    elif config_item == 'roles':
        return VARIABLES.ROLES_SUB_ITEMS
    elif config_item == 'tagCollections':
        return VARIABLES.TAG_COLLECTIONS_SUB_ITEMS
    elif config_item == 'taskDefinitions':
        return VARIABLES.TASK_DEFINITIONS_SUB_ITEMS
    elif config_item == 'tasks':
        return VARIABLES.TASKS_SUB_ITEMS
    elif config_item == 'timedActions':
        return VARIABLES.TIMED_ACTIONS_SUB_ITEMS
    elif config_item == 'userDefinedObjectTypes':
        return VARIABLES.USER_DEFINED_OBJECT_TYPES_SUB_ITEMS
    elif config_item == 'users':
        return VARIABLES.USERS_SUB_ITEMS
    elif config_item == 'variants':
        return VARIABLES.VARIANTS_SUB_ITEMS
    elif config_item == 'wizards':
        return VARIABLES.WIZARDS_SUB_ITEMS
    elif config_item == 'workflowDefinitions':
        return VARIABLES.WORKFLOW_DEFINITIONS_SUB_ITEMS
    elif config_item == 'workflows':
        return VARIABLES.WORKFLOWS_SUB_ITEMS
    elif config_item == 'workspaces':
        return VARIABLES.WORKSPACES_SUB_ITEMS


def get_full_items(config_item, filters: List = [], post_filters: List = [], save: bool = False,
                   with_dependencies: bool = False,
                   log: bool = True, environment: str = "default", cmd: str = None):
    """
    Get full config items, including sub items, with filters.

    TEST STATUS: FULLY TESTED

    :param config_item: config item
    :param filters: filters to apply (from Flex API)
    :param post_filters: custom post-processing filters
    :param save: whether to save the items or not
    :param with_dependencies: whether to also retrieve dependencies
    :param log: whether to log
    :param environment: environment
    :param cmd: cmd mode used
    :return:
    """

    # init possible outputs
    sorted_items = None
    taxonomies = None
    post_processed_sorted_items = None

    # define sub items
    sub_items = enumerate_sub_items(config_item=config_item)

    if cmd == "list":
        final_sub_items = []
        if post_filters:
            for sub_item in sub_items:
                for post_filter in post_filters:
                    if post_filter.startswith(sub_item):
                        final_sub_items.append(sub_item)
        sub_items = set(final_sub_items)

    # switch case
    if config_item == 'accounts':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'actions':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'assets':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'collections':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'eventHandlers':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'events':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'groups':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'jobs':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)

        # do not retrieve surrounding items if cmd is list and items not in post filters
        surrounding_items = ['asset', 'workflow']
        if cmd == "list":
            final_surrounding_items = []
            if post_filters:
                for surrounding_item in surrounding_items:
                    for post_filter in post_filters:
                        if post_filter.startswith(surrounding_item) and get_nested_value(list(sorted_items)[0],
                                                                                         post_filter) is None:
                            final_surrounding_items.append(surrounding_item)
            surrounding_items = final_surrounding_items

        if surrounding_items:
            sorted_items = get_surrounding_items(config_item=config_item, items=sorted_items,
                                                 sub_items=surrounding_items, log=log, environment=environment)
    elif config_item == 'messageTemplates':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'metadataDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'objectTypes':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'profiles':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'quotas':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'resources':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'roles':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'tagCollections':
        # no way to retrieve tags from API directly, so bypassing by reading tags from MD DEFs
        # NOTE: Will only retrieve tags that are used by MD DEFs
        print("\nRetrieving tagCollections from Metadata Definitions as "
              "it is not possible to list them directly from the API...\nPlease note that only tagCollections that are used"
              " in metadata definitions will be retrieved.")
        metadata_definitions = get_items(config_item="metadataDefinitions",
                                         sub_items=VARIABLES.METADATA_DEFINITIONS_SUB_ITEMS, environment=environment)
        sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['tagCollections'],
                                               environment=environment)
    elif config_item == 'taskDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'tasks':
        # add account ID by default otherwise some tasks are missing
        try:
            filters.append(f"accountId={get_default_account_id(environment=environment)}")
        except:
            filters = [f"accountId={get_default_account_id(environment=environment)}"]
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'taxonomies':
        taxonomies = get_taxonomies(filters=filters, environment=environment)
    elif config_item == 'timedActions':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'userDefinedObjectTypes':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'users':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'variants':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'wizards':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'workflowDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
    elif config_item == 'workflows':
        # retrieve workflow variables by default
        filters.append("includeVariables=true") if "includeVariables=false" not in filters else None
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)
        # pull workflow jobs
        if cmd != 'list':
            for item in sorted_items:
                jobs = {}
                for job in tqdm(sorted_items.get(item).get('jobs').get('jobs'),
                                desc=f"Retrieving workflow ID {sorted_items.get(item).get('id')} jobs"):
                    job_id = job.get('id')
                    jobs.update(get_full_items(config_item='jobs', filters=[f'id={job_id}'], log=False,
                                               environment=environment))
                save_items(config_item='jobs', items=jobs, log=False, environment=environment)

    elif config_item == 'workspaces':
        sorted_items = get_items(config_item=config_item, sub_items=sub_items, filters=filters,
                                 with_dependencies=with_dependencies, log=log, environment=environment)

    # post-processing, not available for taxonomies
    if sorted_items and post_filters:
        post_processed_sorted_items = apply_post_retrieval_filters(items=sorted_items, filters=post_filters)

    # save if asked to
    if save and config_item == 'taxonomies':
        save_taxonomies(taxonomies=taxonomies, environment=environment)
    elif save and config_item != 'taxonomies':
        if post_filters:
            save_items(config_item=config_item, items=post_processed_sorted_items, log=log)
        else:
            save_items(config_item=config_item, items=sorted_items, log=log)

    # taxonomies handled differently
    if config_item == 'taxonomies':
        return taxonomies
    elif post_filters:
        return post_processed_sorted_items
    else:
        return sorted_items


def save_items(config_item: str, items: dict, backup: bool = False, log: bool = True, environment: str = "default"):
    """
    Save Flex items to JSON

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param config_item: config item
    :param items: dict of items
    :param backup: whether item is backup or not
    :param log: whether to log
    :param environment: environment
    :return:
    """

    # env folder
    environment = get_default_env_alias() if environment == "default" else environment

    # parent folder
    create_folder(folder_name=environment, ignore_error=True)
    create_folder(folder_name=os.path.join(environment, config_item), ignore_error=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")

    print("") if log else None

    # folder for each config
    for item in items:

        # folder's name
        if config_item == 'events':
            folder_name = f"{items.get(item).get('id')}"
        elif config_item == 'jobs' or config_item == 'tasks' or config_item == 'workflows' or config_item == 'assets':
            folder_name = f"{items.get(item).get('id')}".replace("/", "").replace(":", "")
        else:
            folder_name = f"{items.get(item).get('name')}".replace("/", "").replace(":", "")

        # create object folder
        create_folder(folder_name=os.path.join(environment, config_item, folder_name), ignore_error=True)
        create_folder(folder_name=os.path.join(environment, config_item, folder_name, 'backup'), ignore_error=True)

        if backup:
            create_folder(folder_name=os.path.join(environment, config_item, folder_name, 'backup', now), ignore_error=True)
            folder_name = os.path.join(folder_name, 'backup', now)

        # prevents commit loop
        remove_last_modified_keys(items)

        # save subfields in other files
        if 'configuration' in items.get(item) and items.get(item).get('configuration').get('instance'):
            # if groovy script
            if 'script-contents' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=os.path.join(environment, config_item, folder_name), item_config=items.get(item))
                if items.get(item).get('configuration').get('instance').get('imports', {}).get('jar-url'):
                    with open(os.path.join(environment, config_item, folder_name,'jars.json'), "w") as jars_config:
                        json.dump(items.get(item).get('configuration').get('instance').get('imports').get('jar-url'),
                                  jars_config, indent=2)
                items.get(item).get('configuration').get('instance').pop('script-contents')
            # if jef
            elif 'internal-script' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=os.path.join(environment, config_item, folder_name), item_config=items.get(item))
                if items.get(item).get('configuration').get('instance').get('internal-script', {}).get('internal-jar-url'):
                    with open(os.path.join(environment, config_item, folder_name, 'jars.json'), "w") as jars_config:
                        json.dump(items.get(item).get('configuration').get('instance').get('internal-script').get(
                            'internal-jar-url'), jars_config, indent=2)
                items.get(item).get('configuration').get('instance').pop('internal-script')
            # if groovy decision
            elif 'script_type' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=os.path.join(environment, config_item, folder_name), item_config=items.get(item))
                if items.get(item).get('configuration').get('instance').get('imports', {}).get('jar-url'):
                    with open(os.path.join(environment, config_item, folder_name, 'jars.json'), "w") as jars_config:
                        json.dump(items.get(item).get('configuration').get('instance').get('imports').get('jar-url'),
                                  jars_config, indent=2)
                items.get(item).get('configuration').get('instance').pop('script_type')
            else:
                with open(os.path.join(environment, config_item, folder_name, 'configuration.json'), "w") as item_config:
                    json.dump(obj=items.get(item).get('configuration').get('instance'), fp=item_config, indent=2)
                    items.get(item).pop('configuration')

        if 'asset' in items.get(item) and items.get(item).get('asset'):
            with open(os.path.join(environment, config_item, folder_name, 'asset.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('asset'), fp=item_config, indent=2)
                items.get(item).pop('asset')

        if 'workflowInstance' in items.get(item) and items.get(item).get('workflowInstance'):
            with open(os.path.join(environment, config_item, folder_name, 'workflowInstance.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('workflowInstance'), fp=item_config, indent=2)
                items.get(item).pop('workflowInstance')

        if 'definition' in items.get(item) and items.get(item).get('definition').get('definition'):
            with open(os.path.join(environment, config_item, folder_name, 'definition.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('definition').get('definition'), fp=item_config, indent=2)
                items.get(item).pop('definition')

        if 'body' in items.get(item) and items.get(item).get('body'):
            with open(os.path.join(environment, config_item, folder_name, 'body.html'), "w") as item_config:
                item_config.write(items.get(item).get('body'))
                items.get(item).pop('body')

        if 'workflow' in items.get(item) and items.get(item).get('workflow'):
            with open(os.path.join(environment, config_item, folder_name, 'workflow.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('workflow'), fp=item_config, indent=2)
                items.get(item).pop('workflow')

        if 'properties' in items.get(item) and items.get(item).get('properties').get('accountProperties'):
            with open(os.path.join(environment, config_item, folder_name, 'properties.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('properties').get('accountProperties'), fp=item_config, indent=2)
                items.get(item).pop('properties')

        if 'references' in items.get(item) and items.get(item).get('references').get('objects'):
            with open(os.path.join(environment, config_item, folder_name, 'references.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('references').get('objects'), fp=item_config, indent=2)
                items.get(item).pop('references')

        if 'metadata' in items.get(item) and items.get(item).get('metadata').get('instance'):
            with open(os.path.join(environment, config_item, folder_name, 'metadata.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('metadata').get('instance'), fp=item_config, indent=2)
                items.get(item).pop('metadata')

        if 'fileInformation' in items.get(item) and items.get(item).get('fileInformation'):
            with open(os.path.join(environment, config_item, folder_name, 'fileInformation.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('fileInformation'), fp=item_config, indent=2)
                items.get(item).pop('fileInformation')

        if 'assetContext' in items.get(item) and items.get(item).get('assetContext'):
            with open(os.path.join(environment, config_item, folder_name, 'assetContext.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('assetContext'), fp=item_config, indent=2)
                items.get(item).pop('assetContext')

        if 'members' in items.get(item) and items.get(item).get('members').get('users'):
            with open(os.path.join(environment, config_item, folder_name, 'members.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('members').get('users'), fp=item_config, indent=2)
                items.get(item).pop('members')

        if 'role' in items.get(item) and items.get(item).get('role'):
            with open(os.path.join(environment, config_item, folder_name, 'role.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('role'), fp=item_config, indent=2)
                items.get(item).pop('role')
        # todo: convert permissions to dataframe
        if 'permissions' in items.get(item) and items.get(item).get('permissions'):
            with open(os.path.join(environment, config_item, folder_name, 'permissions.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('permissions'), fp=item_config, indent=2)
                items.get(item).pop('permissions')

        if 'hierarchy' in items.get(item) and items.get(item).get('hierarchy'):
            with open(os.path.join(environment, config_item, folder_name, 'hierarchy.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('hierarchy'), fp=item_config, indent=2)
                items.get(item).pop('hierarchy')

        if 'structure' in items.get(item) and items.get(item).get('structure'):
            if VARIABLES.RENDER_WORKFLOW_GRAPHS:
                render_workflow(workflow_structure=items.get(item).get('structure'),
                                save_to=os.path.join(environment, config_item, folder_name))
            with open(os.path.join(environment, config_item, folder_name, 'structure.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('structure'), fp=item_config, indent=2)
                items.get(item).pop('structure')

        if 'variables' in items.get(item) and items.get(item).get('variables'):
            with open(os.path.join(environment, config_item, folder_name, 'variables.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('variables'), fp=item_config, indent=2)
                items.get(item).pop('variables')

        if 'jobs' in items.get(item) and items.get(item).get('jobs').get('jobs'):
            with open(os.path.join(environment, config_item, folder_name, 'jobs.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('jobs').get('jobs'), fp=item_config, indent=2)
                items.get(item).pop('jobs')

        if 'history' in items.get(item) and items.get(item).get('history'):
            history = items.get(item).get('history').copy()
            for idx, logs in enumerate(history.get('events')):
                history.get('events')[idx].pop('object')
                history.get('events')[idx].pop('user')
            with open(os.path.join(environment, config_item, folder_name, 'history.json'), "w") as item_config:
                json.dump(obj=items.get(item).get('history'), fp=item_config, indent=2)
                items.get(item).pop('history')

        if 'status' in items.get(item) and items.get(item).get('taskDefinition'):
            with open(os.path.join(environment, config_item, folder_name, 'status.json'), "w") as item_config:
                json.dump(obj={'status': items.get(item).get('status')}, fp=item_config, indent=2)
                items.get(item).pop('status')

        try:
            if 'relationships' in items.get(item) and items.get(item).get('relationships').get('relationships'):
                with open(os.path.join(environment, config_item, folder_name, 'relationships.json'), "w") as item_config:
                    json.dump(obj=items.get(item).get('relationships').get('relationships'), fp=item_config, indent=2)
                    items.get(item).pop('relationships')
        except:
            pass

        if 'lastPollTime' in items.get(item):
            items.get(item).pop("lastPollTime")

        if 'revision' in items.get(item):
            items.get(item).pop('revision')

        # save main object
        with open(os.path.join(environment, config_item, folder_name, '_object.json'), "w") as item_config:
            json.dump(obj=items.get(item), fp=item_config, indent=2)

    print(f"{environment}/{config_item} have been retrieved successfully. \n") if items and log else None


def save_taxonomies(taxonomies, environment: str = "default"):
    """
    Save taxonomies.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param taxonomies: taxonomies
    :param environment: environment
    :return:
    """

    # get env url if default
    environment = get_default_env_alias() if environment == "default" else environment

    # create parent folders
    create_folder(folder_name=environment, ignore_error=True)
    create_folder(folder_name=os.path.join(environment, 'taxonomies'), ignore_error=True)

    print("")

    for idx, taxonomy in enumerate(taxonomies):
        # create taxonomy folder
        create_folder(folder_name=os.path.join(environment, 'taxonomies', str(taxonomy.get('name'))), ignore_error=True)

        # removed useless keys
        remove_last_modified_keys(taxonomies)

        # save taxonomy
        with open(os.path.join(environment, 'taxonomies', taxonomy.get('name'), '_object.json'), "w") as item_config:
            json.dump(obj=taxonomies[idx], fp=item_config, indent=2)
            print(f"{environment}/taxonomies: {taxonomy.get('name')} has been retrieved successfully. ")

    print("") if taxonomies else None


def get_nested_value(obj, keys):
    """
    Get nested value for a given key separater by '.'

    TEST STATUS: FULLY TESTED

    :param obj: obj to search the value in
    :param keys: sequence of keys separater by '.'
    """

    for key in keys.split('.'):
        if '[' in key and ']' in key:
            if '[text]' in key:
                return str(obj[key.split('[text]')[0]])
            elif re.search(r"\[-?\d+\]", key):
                match = int(re.search(r'\[-?\d+\]', key).group(0)[1:-1])
                # skip if error from API
                try:
                    obj = obj[key.split('[')[0]][-match]
                except:
                    return None
        elif isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            return None
    return obj


def get_surrounding_items(config_item: str, items: dict, sub_items: List[str], log: bool = True,
                          environment: str = "default"):
    """
    Get surrounding items of a config item.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param log:
    :param config_item: config item
    :param items: items to get the sub_items of
    :param sub_items: surrounding items to get
    :param environment: environment
    :return:
    """

    for item in tqdm(items, desc=f"Retrieving {config_item} {str(sub_items)}", disable=not log):

        # asset
        if 'asset' in sub_items:
            try:
                asset_id = items.get(item).get('asset').get('id')
                asset = query(method="GET", url=f"assets/{asset_id};includeMetadata=true", log=False,
                              environment=environment)
                items[item]['asset'] = asset
            except:
                pass

        # workflow
        if 'workflow' in sub_items:
            try:
                workflow_id = items.get(item).get('workflow').get('id')
                workflow_instance = query(method="GET", url=f"workflows/{workflow_id}", log=False,
                                          environment=environment)
                workflow_variables = query(method="GET", url=f"workflows/{workflow_id}/variables", log=False,
                                           environment=environment)
                items[item]['workflow'] = workflow_instance
                items[item]['workflow']['variables'] = workflow_variables
            except:
                pass

    return items


def find_and_pull_dependencies(json_config: {}):
    """
    Find and pull dependencies.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :return:
    """

    # find dependencies
    dependencies = find_nested_dependencies(json_config)

    for dependency in dependencies:

        # get dependency info
        tmp = json_config.copy()
        for subpath in dependency.split("."):
            # index of list
            if subpath.isdigit():
                tmp = tmp[int(subpath)]
            else:
                tmp = tmp.get(subpath).copy()

        # fetch dependency
        if 'actionType' in tmp:  # actions in workflowDefinitions
            config_item = "actions"
        elif 'objectType' in tmp:  # tasks in workflowDefinitions
            config_item = "taskDefinitions"
        else:
            config_item = kebab_to_camel_case(tmp.get('type'))
        get_full_items(config_item=config_item, filters=[f"name={tmp.get('name')}", "exactNameMatch=true"], save=True,
                       log=False)

    return dependencies


def find_nested_dependencies(data, parent_key='', separator='.'):
    """
    Find dependencies in a JSON item config.

    TEST STATUS: FULLY TESTED

    :param data:
    :param parent_key:
    :param separator:
    :return:
    """

    paths = []

    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            if 'id' in value:
                paths.append(new_key)
            paths.extend(find_nested_dependencies(value, new_key, separator))

        if isinstance(value, list):
            for idx, list_item in enumerate(value):
                if new_key != "transitions":
                    paths.extend(find_nested_dependencies(value[idx], new_key + f".{idx}", separator))

    # remove actionType and objectType as we don't want to pull these
    filtered_paths = list(filter(lambda x: not re.compile(r'.*Type.*').match(x), paths))

    return filtered_paths


def get_taxonomies(filters: List[str], log: bool = True, environment: str = "default"):
    """
    Get taxonomies from public API

    TEST STATUS: FULLY TESTED

    :param environment: environment
    :param filters: filters to apply
    :param log: whether to log
    :return:
    """

    # encode fql
    if filters:
        for idx, filter in enumerate(filters):
            if "fql=" in filter:
                filters[idx] = "fql=" + urllib.parse.quote(filter.replace("fql=", ""))

    # get total count
    taxonomies = query(method="GET", url=f"taxonomies{';' + ';'.join(filters) if filters else ''}", log=log,
                       environment=environment)

    enabled_taxonomies = []
    for idx, taxonomy in enumerate(taxonomies):
        if taxonomy['enabled']:
            enabled_taxonomies.append(taxonomies[idx])

    # get taxons
    taxonomies = get_taxons(taxonomies=enabled_taxonomies, environment=environment)

    return taxonomies


def get_taxons(taxonomies: List[dict], environment: str = "default", url: str = None):
    """
    Get taxonomies' taxons - recursively

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param taxonomies: taxonomies
    :param environment: environment
    :param url: url
    :return:
    """

    # this one is pretty hard to understand
    for idx, taxonomy in enumerate(taxonomies):

        # build and send api call
        root_taxons_request = f"taxonomies/{taxonomy['id']}/taxons" if not url else url
        taxonomies[idx]['childTaxons'] = query(method="GET", url=f"{root_taxons_request}", log=False,
                                               environment=environment)

        try:
            # for root taxons' children (childTaxons)
            for idx2, child_taxon in enumerate(taxonomies[idx]['childTaxons']):
                # only retrieve the enabled ones
                if taxonomies[idx]['childTaxons'][idx2]['enabled']:
                    # check for children recursively if root taxon child has children
                    if taxonomies[idx]['childTaxons'][idx2]['hasChildren']:
                        taxonomies[idx]['childTaxons'][idx2]['childTaxons'] = get_taxons(
                            taxonomies=[taxonomies[idx]['childTaxons'][idx2].copy()],
                            environment=environment,
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
                            environment=environment,
                            url=f"{root_taxons_request.split('taxons/')[0]}taxons/{taxonomies[idx]['childTaxons']['taxons'][idx2]['id']}/taxons"
                        )[0]['childTaxons']['taxons']

    return taxonomies


def get_tags_and_taxonomies(metadata_definitions: dict, save_to: str = "",
                            mode: List[str] = ['tagCollections', 'taxonomies'], environment: str = "default"):
    """
    Get taxonomies and tags from metadata def configs.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param mode: which items to retrieve
    :param metadata_definitions: dict of metadata defs
    :param save_to: where to save the config
    :param environment: environment to get the tags and taxonomies from
    """

    # init. tax & tags
    taxonomies = []
    tags = []

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
            tag_collection = query(method="GET", url=f"tagCollections/{tag}", log=False, environment=environment)
            tag_dict[tag_collection['displayName']] = tag_collection

        # sort
        sorted_tag_dict = {i: tag_dict[i] for i in sorted(list(tag_dict.keys()))}

    # fetch taxonomies
    if 'taxonomies' in mode:
        tax_dict = dict()
        for tax in tqdm(set(taxonomies), desc=f"Retrieving taxonomies"):
            # get taxonomies
            taxonomy = query(method="GET", url=f"taxonomies/{tax}", log=False, environment=environment)
            try:
                tax_dict[taxonomy['displayName']] = taxonomy
            except:
                continue

        # sort
        sorted_tax_dict = {i: tax_dict[i] for i in sorted(list(tax_dict.keys()))}

    # save tags as JSON
    if save_to and 'tagCollections' in mode:
        with open(os.path.join(save_to, 'configs', 'tags.json'), "w") as tags_config:
            json.dump(obj=sorted_tag_dict, fp=tags_config, indent=2)
            print(f"tags have been saved to {save_to}/configs/tags.json")

    # save taxonomies as JSON
    if save_to and 'taxonomies' in mode:
        with open(os.path.join(save_to, 'configs', 'taxonomies.json'), "w") as taxonomies_config:
            json.dump(obj=sorted_tax_dict, fp=taxonomies_config, indent=2)
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

    TEST STATUS: FULLY TESTED

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

    TEST STATUS: FULLY TESTED

    :return:
    """

    # retrieve default env
    env = get_env(environment=environment)

    # init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=decrypt_pwd(pwd=env['password']))

    return env, auth


def query(method: str, url: str, payload=None, log: bool = True, environment: str = "default") -> Union[dict, list]:
    """
    Query the public API.

    TEST STATUS: FULLY TESTED

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
    )

    # response is json
    try:
        query_result = query_result.json()
    except Exception as ex:
        # response is list
        if isinstance(query_result, list):
            pass
        else:
            raise TypeError(f"{ex}: {query_result}")

    # exception handler
    if isinstance(query_result, dict) and 'errors' in query_result:
        raise AttributeError(
            f"\n\nError while sending {query}. \nError message: {str(query_result['errors'])}\n ")

    return query_result


def create_script(item_name, item_config):
    """
    Create groovy script with according imports and plugins.

    TEST STATUS: FULLY TESTED

    :param item_name: script name
    :param item_config: script config
    :return:
    """

    imports = ["import com.ooyala.flex.plugins.PluginCommand\n"]
    script = "class Script extends PluginCommand {\n    <&code>\n}"

    # jef
    try:
        imports.extend(['import ' + imp['value'] + '\n' for imp in
                        item_config['configuration']['instance']['internal-script']['script-import']])
    except:
        pass

    try:
        imports.extend(['import ' + imp['value'] + '\n' for imp in
                        item_config['configuration']['instance']['imports']['import']])
    except:
        pass

    # groovy decision
    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['script_type']['script'].replace("\n",
                                                                                                          "\n    "))
    except:
        pass

    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['internal-script']['script-content'].replace(
                                    "\n", "\n    "))
    except:
        pass

    # groovy script
    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['script-contents']['script'].replace("\n",
                                                                                                              "\n    "))
    except:
        script = script.replace("<&code>", "")

    content = f"{''.join(imports)}\n{script}"

    with open(os.path.join(item_name, 'script.groovy'), "w") as groovy_file:
        groovy_file.write(content)

    return content


def kebab_to_camel_case(string):
    """
    Kebab to Camel Case.

    TEST STATUS: FULLY TESTED

    :param string: string to convert
    :return:
    """

    words = string.split('-')
    camel_case_words = [words[0]] + [word.capitalize() for word in words[1:]]
    camel_case = ''.join(camel_case_words)

    return camel_case + 's'


def remove_last_modified_keys(input_dict):
    """
    Remove "lastModified" keys in JSON API responses for Bitbucket.

    TEST STATUS: FULLY TESTED

    :param input_dict:
    :return:
    """
    if isinstance(input_dict, dict):
        for key in list(input_dict.keys()):
            if "lastModified" in key:
                del input_dict[key]
            else:
                remove_last_modified_keys(input_dict[key])
    elif isinstance(input_dict, list):
        for item in input_dict:
            remove_last_modified_keys(item)


def render_workflow(workflow_structure: dict, save_to: str):
    """
    Render workflows using graphviz.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param workflow_structure: dict of workflows
    :param save_to: where to save the workflow graphs
    """

    # Init. graph
    graph = graphviz.Digraph(name=f"graph", directory=f"{save_to}")

    try:
        # Create nodes with images
        for node in workflow_structure['nodes']:
            label, style, color = config_node(node)
            graph.node(name=escape(node['name']), label=label, shape="box", style=style,
                       fillcolor=color)

        # Create edges with names
        for transition in workflow_structure['transitions']:
            graph.edge(escape(transition['from']['name']),
                       escape(transition['to']['name']),
                       label=transition['name'] if not None else None)
    except KeyError:
        pass

    # Render graph
    graph.render(filename=f"graph", engine="dot", format="png")


def config_node(node: dict) -> tuple[str, str, str]:
    """
    Build node label with name, image and style.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param node: json dict of the node
    """

    # Init. node image and reformat node name
    node_image = ""
    node_name = escape(node.get('name'))
    node_style = "filled"
    node_color = ""
    node_action = ""

    # Style map nodes
    if "objectType" in node:
        # Workflow
        if node['objectType']['name'] == "workflow-definition":
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'workflow.png')
            node_color = "GhostWhite"
        # Wizard
        elif node['objectType']['name'] == "wizard":
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'wizard.png')
            node_color = "Yellow"
        # Resource
        elif node['objectType']['name'] == 'resource':
            if node['resourceSubType'] == 'Inbox':
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'resource-inbox.png')
                node_color = "Lavender"
            else:
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'resource-hot-folder.png')
                node_color = "LightBlue"
        # Event Handler
        elif node['objectType']['name'] == 'event-handler':
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'event-handler.png')
            node_color = "Grey"
        # Launch Action
        elif node['objectType']['name'] == 'action':
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'workflow.png')
            node_color = "GhostWhite"
            try:
                node_name = escape(node['configuration']['instance']['workflows'][0]['Workflow']['name'])
            except KeyError:
                node_name = escape(node['configuration']['instance']['Workflow']['name'])
        # Timed Action
        elif node['objectType']['name'] == 'timed-action':
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'timed-action.png')
            node_color = "DarkGrey"

    # Style workflow nodes
    elif "type" in node:
        if node['type'] == "ACTION":
            node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', node["action"]["type"].lower() + ".png")
            node_color = "GhostWhite"
            node_action = escape(node["action"]["name"])
        else:
            if node["type"] == "START":
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'start.png')
                node_color = "LightGreen"
            if node["type"] == "END":
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'end.png')
                node_color = "LightCoral"
            if node["type"] == "FORK":
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons','fork.png')
            if node["type"] == "JOIN":
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'join.png')
            if node["type"] == "TASK":
                node_image = os.path.join(os.environ.get('FTBX'), 'flex-icons', 'task.png')
                node_color = "LightYellow"

    # Build label
    node_label = f"""<<table cellspacing="0" border="0" cellborder="0"><tr><td><img src="{node_image}" /></td><td> {node_name if not node_action else node_action}</td></tr></table>>"""

    return node_label, node_style, node_color


def escape(string: str) -> str:
    """
    Custom string escape

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param string:
    :return:
    """

    return re.sub(r'[^a-zA-Z0-9-_ ]', '', string)


def str_to_bool(string: str):
    """
    Converts strings to bool ()

    TEST STATUS: FULLY TESTED

    :param string: from [false, False, true, True]
    :return:
    """

    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False
    else:
        raise ValueError(f"String is not a valid boolean (input: {string}, expected: [false, False, true, True])")


def convert_to_native_type(string: str):
    """
    Converts a string to its most likely type.

    TEST STATUS: FULLY TESTED

    :param string: a string
    :return:
    """

    try:
        # int first
        return int(string)
    except ValueError:
        try:
            # float
            return float(string)
        except ValueError:
            # finally bool
            if string.lower() == 'true':
                return True
            elif string.lower() == 'false':
                return False
            else:
                # default to str
                return string


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
