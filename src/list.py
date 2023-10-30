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

from src.utils import get_full_items, apply_post_retrieval_filters


def list_command_func(args):
    """Action on list command. """

    list_items(config_item=args.config_item, filters=args.filters, post_filters=args.post_filters)


def list_items(config_item: str, filters: List[str] = [], post_filters: List[str] = []) -> bool:
    """
    List items ids.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param filters: filters to apply
    :param post_filters: post retrieval filters

    :return: True if succeeds, False if fails
    """

    # init displayed content
    log_fields = []

    # get items
    sorted_items = get_full_items(config_item=config_item, filters=filters, post_filters=post_filters)

    # switch case
    if config_item == 'accounts':
        log_fields = ['name', 'id']
    elif config_item == 'actions':
        log_fields = ['name', 'id', 'type.name']
    elif config_item == 'assets':
        log_fields = ['name', 'id', 'variant.name', 'variant.id']
    elif config_item == 'collections':
        log_fields = ['name', 'uuid']
    elif config_item == 'eventHandlers':
        log_fields = ['name', 'id', 'configuration.instance.action-config.name',
                      'configuration.instance.action-config.id']
    elif config_item == 'events':
        log_fields = ['time', 'id', 'eventType', 'message']
    elif config_item == 'groups':
        log_fields = ['name', 'id', 'role.name', 'role.id']
    elif config_item == 'jobs':
        log_fields = ['name', 'id', 'status', 'actionType.name', 'asset.id', 'workflow.id']
    elif config_item == 'messageTemplates':
        log_fields = ['name', 'id']
    elif config_item == 'metadataDefinitions':
        log_fields = ['name', 'id']
    elif config_item == 'objectTypes':
        log_fields = ['name', 'id']
    elif config_item == 'profiles':
        log_fields = ['name', 'id', 'type']
    elif config_item == 'quotas':
        log_fields = ['name', 'id']
    elif config_item == 'resources':
        log_fields = ['name', 'id', 'resourceType', 'resourceSubType', 'status']
    elif config_item == 'roles':
        log_fields = ['name', 'id']
    elif config_item == 'tagCollections':
        log_fields = ['name', 'id']
    elif config_item == 'taskDefinitions':
        log_fields = ['name', 'id']
    elif config_item == 'tasks':
        log_fields = ['name', 'id', 'status', 'asset.name', 'asset.id']
    elif config_item == 'taxonomies':
        log_fields = ['name', 'id']
    elif config_item == 'timedActions':
        log_fields = ['name', 'id', 'status', 'interval']
    elif config_item == 'userDefinedObjectTypes':
        log_fields = ['name', 'id']
    elif config_item == 'users':
        log_fields = ['displayName', 'id', 'userType', 'email', 'lastLoggedIn']
    elif config_item == 'variants':
        log_fields = ['name', 'id', 'defaultMetadataDefinition.displayName', 'defaultMetadataDefinition.id']
    elif config_item == 'wizards':
        log_fields = ['name', 'id']
    elif config_item == 'workflowDefinitions':
        log_fields = ['name', 'id', ]
    elif config_item == 'workflows':
        log_fields = ['name', 'id', 'status', 'asset.name', 'asset.id']
    elif config_item == 'workspaces':
        log_fields = ['name', 'id']
    elif config_item == 'all':
        print("This command is not avaiable. ")
        quit()

    # add post_filters to displayed data if not script (otherwise unreadable)
    if post_filters:
        for post_filter in post_filters:
            if "script" not in post_filter:
                log_fields.append(post_filter)

    # readability
    print("")

    # convert to dataframe and display
    # taxonomies are handled differently because the API response is different
    if config_item == 'taxonomies':
        rows = []
        columns = log_fields
        columns.append('taxons [id]')
        for idx, taxonomy in enumerate(sorted_items):
            row = [taxonomy['name'], taxonomy['id']]
            if 'childTaxons' in taxonomy:
                child_taxons = []
                for idx2, child_taxon in enumerate(taxonomy['childTaxons']):
                    child_taxons.append(
                        f"{taxonomy['childTaxons'][idx2]['name']} [{taxonomy['childTaxons'][idx2]['id']}]")
                row.append(", ".join(child_taxons))
            rows.append(row)

        # display dataframe
        table = pd.DataFrame(rows, columns=columns)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)
        table.index += 1
        pd.DataFrame.to_csv(table, "list.csv")
        print(table)

        # save result as JSON for further details
        with open('list.json', 'w') as result_file:
            json.dump(sorted_items, result_file, indent=4)
            print(
                "\nResults of the query (with nested taxons) have been saved as list.json for your best convenience.\n")

    else:
        rows = []
        columns = log_fields
        if sorted_items:
            for item in sorted_items:
                row = []

                # extract field
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

            # display dataframe
            table = pd.DataFrame(rows, columns=columns)
            pd.set_option('display.colheader_justify', 'center')
            pd.set_option('display.max_colwidth', None)
            pd.set_option('display.max_rows', None)
            table.index += 1
            pd.DataFrame.to_csv(table, "list.csv")
            print(table)

            # save result as JSON for further details
            with open('list.json', 'w') as result_file:
                json.dump(sorted_items, result_file, indent=4)
                print("\nResults of the query have been saved as list.json for your best convenience.\n")

        # empty results from API
        else:
            print(f"No {config_item} found for the given parameters.\n")

    return True
