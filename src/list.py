"""

    PROJECT: flex_toolbox
    FILENAME: list.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: list command functions
    
"""
import json
from typing import List

import pandas as pd
import requests

from src.utils import get_items, get_tags_and_taxonomies

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# Init. session
session = requests.Session()


def list_command_func(args):
    """Action on list command. """

    list_items(config_item=args.config_item, filters=args.filters)


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
        # No way to retrieve tags from API directly, so bypassing by reading tags from MD DEFs
        # NOTE: Will only retrieve tags that are used by MD DEFs
        print("\nRetrieving tagCollections from Metadata Definitions as "
              "it is not possible to list them directly from the API...\nPlease note that only tagCollections that are used"
              " in metadata definitions will be retrieved.")
        metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
        sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['tagCollections'])
        log_fields = ['name', 'id']
    elif config_item == 'taskDefinitions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'tasks':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'asset.name', 'asset.id']
    elif config_item == 'taxonomies':
        # No way to retrieve taxonomies from API directly, so bypassing by reading tags from MD DEFs
        # NOTE: Will only retrieve taxonomies that are used by MD DEFs
        print("\nRetrieving taxonomies from Metadata Definitions as "
              "it is not possible to list them directly from the API...\nPlease note that only taxonomies that are used"
              " in metadata definitions will be retrieved.")
        metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
        sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['taxonomies'])
        log_fields = ['name', 'id']
    elif config_item == 'timedActions':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id', 'status', 'interval']
    elif config_item == 'userDefinedObjectTypes':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['name', 'id']
    elif config_item == 'users':
        sorted_items = get_items(config_item=config_item, filters=filters)
        log_fields = ['displayName', 'id', 'userType', 'email', 'lastLoggedIn']
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

        # Save result as JSON for further details
        with open('list.json', 'w') as result_file:
            json.dump(sorted_items, result_file, indent=4)
            print("\nResults of the query have been saved as list.json for your best convenience.")

    # Empty results from API
    else:
        print(f"No {config_item} found for the given parameters. ")
    print("")

    return True
