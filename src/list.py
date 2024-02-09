"""

    PROJECT: flex_toolbox
    FILENAME: list.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: list command functions

    TEST STATUS: FULLY TESTED
"""
import json
import os
import re
import datetime
from typing import List

import pandas as pd

from src.env import get_default_env_alias
from src.utils import get_full_items, create_folder


def list_command_func(args):
    """
    Action on list command.

    TEST STATUS: FULLY TESTED
    """

    filename = list_items(config_item=args.config_item, filters=args.filters, post_filters=args.post_filters, environment=args.from_)

    return filename


def list_items(config_item: str, filters: List[str] = [], post_filters: List[str] = [],
               environment: str = "default") -> str:
    """
    List items ids.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param environment: environment
    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param filters: filters to apply
    :param post_filters: post retrieval filters

    :return: True if succeeds, False if fails
    """

    # init displayed content
    log_fields = []

    # add exactNameMatch=true when name is provided
    if filters:
        if any('name=' in f for f in filters) and not any('fql' in f for f in filters):
            filters.append('exactNameMatch=true')

    # get items
    sorted_items = get_full_items(config_item=config_item, filters=filters, post_filters=post_filters, environment=environment, cmd="list")

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
        log_fields = ['name', 'id', 'status', 'progress', 'actionType.name', 'asset.id', 'workflow.id']
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
        print("This command is not available. ")
        quit()

    # add post_filters to displayed data if not script (otherwise unreadable)
    if post_filters:
        for post_filter in post_filters:
            if "script" not in post_filter:
                for op in ['!=', '>=', '<=', '~', '=', '<', '>']:
                    if op in post_filter:
                        post_filter = post_filter.split(op)[0]
                        log_fields.append(post_filter)
                        break

    # readability
    print("")

    # build CSV and JSON filenames
    create_folder(folder_name='lists', ignore_error=True)
    dt = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{dt}_{get_default_env_alias()}_{config_item}{'_' + '_'.join(filters) if filters else ''}{'_' + '_'.join(post_filters) if post_filters else ''}"
    filename = clean_filename(filename)
    filename = os.path.join('lists', filename)

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
        pd.DataFrame.to_csv(table, f"{filename}.csv")
        print(table)

        # save result as JSON for further details
        with open(f'{filename}.json', 'w') as result_file:
            json.dump(sorted_items, result_file, indent=4)
            print("\nResults of the query have been saved in lists/ for your best convenience.\n")

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
                                if "[" in subfield and "]" in subfield:
                                    if '[text]' in subfield:
                                        tmp = tmp.get(str(subfield.split('[')[0]))
                                    elif re.search(r"\[-?\d+\]", subfield):
                                        match = int(re.search(r'\[-?\d+\]', subfield).group(0)[1:-1])
                                        tmp = tmp.get(subfield.split('[')[0])[-match]
                                else:
                                    tmp = tmp.get(subfield)
                                    # replace line breaks otherwise csv is broken
                                    if isinstance(tmp, str):
                                        tmp = tmp.replace("\n", " ")
                            except:
                                pass
                        row.append(str(tmp))
                rows.append(row)

            # display dataframe
            table = pd.DataFrame(rows, columns=columns)
            table = table.loc[:, ~table.columns.duplicated()]
            pd.set_option('display.colheader_justify', 'center')
            pd.set_option('display.max_colwidth', 75)
            pd.set_option('display.max_rows', 50)
            table.index += 1
            pd.DataFrame.to_csv(table, f"{filename}.csv")
            print(table)

            # save result as JSON for further details
            with open(f'{filename}.json', 'w') as result_file:
                json.dump(sorted_items, result_file, indent=4)
                print("\nResults of the query have been saved in lists/ for your best convenience.\n")

        # empty results from API
        else:
            print(f"No {config_item} found for the given parameters.\n")

    return filename


def clean_filename(filename: str):
    """
    Clean filename of special characters.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param filename: filename to clean
    """

    filename = filename.replace('\\', '-') \
        .replace(":", '-') \
        .replace("/", '-') \
        .replace("*", '-') \
        .replace("?", 'Q') \
        .replace("\"", '-') \
        .replace("<=", 'LTE') \
        .replace("<", 'LT') \
        .replace(">=", 'GTE') \
        .replace(">", 'GT')

    return filename
