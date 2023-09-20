"""

    PROJECT: flex_toolbox
    FILENAME: list.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
from typing import List

import requests
import pandas as pd

from src.utils import get_items

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. session
session = requests.Session()


def list_command_func(args):
    """Action on list command. """

    list_items(config_item=args.config_item, filters=args.filters)

    # collections

    # ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
    #               'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
    #               'tagsCollections', 'taskDefinitions', 'tasks', 'taxonomies', 'taxonomies', 'timedActions',
    #               'userDefinedObjectTypes',
    #               'users', 'variants', 'variants', 'wizards', 'workflowDefinitions', 'workflows', 'workspaces']

    # TODO: custom for userDefinedObject, tagCollections


def list_items(config_item: str, filters: List[str] = []) -> bool:
    """
    List items ids.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param filters: filters to apply

    :return: True if succeeds, False if fails
    """

    sorted_items = {}
    log_fields = []

    if config_item == 'accounts':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'actions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'assets':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'variant.name', 'variant.id']
    elif config_item == 'collections':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'uuid']
    elif config_item == 'eventHandlers':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        log_fields = ['name', 'id', 'configuration.instance.action-config.name',
                      'configuration.instance.action-config.id']
    elif config_item == 'events':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['time', 'id', 'eventType', 'message']
    elif config_item == 'groups':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'role.name', 'role.id']
    elif config_item == 'jobs':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'asset.id', 'workflow.id']
    elif config_item == 'messageTemplates':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'metadataDefinitions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'objectTypes':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'profiles':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'type']
    elif config_item == 'quotas':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'resources':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'resourceType', 'resourceSubType', 'status']
    elif config_item == 'roles':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'tagCollections':
        sorted_items = get_items(config_item=config_item, filters=filters, prefix='metadata')
        log_fields = ['name', 'id']
    elif config_item == 'taskDefinitions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'tasks':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'asset.name', 'asset.id']
    elif config_item == 'taxonomies':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'timedActions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'interval']
    elif config_item == 'userDefinedObjectTypes':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'users':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'userType', 'email', 'lastLoggedIn']
    elif config_item == 'variants':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'defaultMetadataDefinition.displayName', 'defaultMetadataDefinition.id']
    elif config_item == 'wizards':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'workflowDefinitions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', ]
    elif config_item == 'workflows':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'asset.name', 'asset.id']
    elif config_item == 'workspaces':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']

    print("")

    # Convert to dataframe and display
    rows = []
    columns = log_fields
    if sorted_items:
        for item in sorted_items:
            row = []

            # Extract field
            for field in log_fields:
                if "." not in field:
                    row.append(str(sorted_items.get(item).get(field)))
                else:
                    tmp = sorted_items.get(item)
                    for subfield in field.split("."):
                        try:
                            tmp = tmp.get(subfield)
                        except:
                            pass
                    row.append(str(tmp))
            rows.append(row)

        # Display dataframe
        table = pd.DataFrame(rows, columns=columns)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_colwidth', None)
        table.index += 1
        print(table)

    # Empty results from API
    else:
        print(f"No {config_item} found for the given parameters. ")
    print("")

    return True
