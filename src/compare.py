"""

    PROJECT: flex_toolbox
    FILENAME: compare.py
    AUTHOR: David NAISSE
    DATE: October 17, 2023

    DESCRIPTION: compare command functions

"""
import json

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.utils import get_items, create_folder


def compare_command_func(args):
    """Action on pull command. """

    if len(args.environments) >= 2:
        # compare_items(config_item=args.config_item, environments=args.environments, filters=args.filters)
        compare_items(config_item=args.config_item, environments=args.environments, filters=args.filters,
                      sub_items=['configuration'])
        # todo:
        #   - compare all items for a config item
        #   - add more granular compare with config and sub_items
    else:
        print(
            f"Cannot compare {args.config_item} if number of environments provided is less than 2 (provided: {args.environments}). ")


#
# def compare_items(config_item: str, environments: list, filters: list = []):
#     """
#     Compare items between envs.
#
#     :param config_item: config item
#     :param environments: list of envs
#     :param filters: filters to apply
#     :return:
#     """
#
#     if config_item == 'accounts':
#         sorted_items = get_items(config_item=config_item, sub_items=['metadata', 'properties'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'actions':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'assets':
#         sorted_items = get_items(config_item=config_item, sub_items=['metadata'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'collections':
#         sorted_items = get_items(config_item=config_item, sub_items=['metadata'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'eventHandlers':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'events':
#         sorted_items = get_items(config_item=config_item, filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'groups':
#         sorted_items = get_items(config_item=config_item, sub_items=['members'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'jobs':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration', 'history'], filters=filters)
#         sorted_items = get_surrounding_items(config_item=config_item, items=sorted_items,
#                                              sub_items=['asset', 'workflow'])
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'messageTemplates':
#         sorted_items = get_items(config_item=config_item, sub_items=['body'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'metadataDefinitions':
#         sorted_items = get_items(config_item=config_item, sub_items=['definition'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'objectTypes':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'profiles':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'quotas':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'resources':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'roles':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'tagCollections':
#         # no way to retrieve tags from API directly, so bypassing by reading tags from MD DEFs
#         # NOTE: Will only retrieve tags that are used by MD DEFs
#         print("\nRetrieving tagCollections from Metadata Definitions as "
#               "it is not possible to list them directly from the API...\nPlease note that only tagCollections that are used"
#               " in metadata definitions will be retrieved.")
#         metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
#         sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['tagCollections'])
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'taskDefinitions':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'tasks':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'taxonomies':
#         taxonomies = get_taxonomies(filters=filters)
#         save_taxonomies(taxonomies=taxonomies)
#     elif config_item == 'timedActions':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'userDefinedObjectTypes':
#         sorted_items = get_items(config_item=config_item, sub_items=['hierarchy', 'relationships'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'users':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'variants':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'wizards':
#         sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'workflowDefinitions':
#         sorted_items = get_items(config_item=config_item, sub_items=['structure'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'workflows':
#         sorted_items = get_items(config_item=config_item, sub_items=['variables', 'jobs'], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)
#     elif config_item == 'workspaces':
#         sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
#         save_items(config_item=config_item, items=sorted_items)


def compare_items(config_item: str, filters: list, environments: list, local: bool = False, sub_items: list = []):
    """
    Compare items between environments.

    :param sub_items: sub items
    :param local: whether to use local comparison or not
    :param config_item: config item (ex: actions, workflowDefinitions)
    :param filters: filters to apply
    :param environments: envs (ex: customer-dev, customer-stg, customer-prod)
    :return:
    """

    cmp = {}
    tmp_compare = {}
    df = None

    # create compare folder
    create_folder(folder_name="compare", ignore_error=True)

    # get item from envs
    for env in environments:
        items = get_items(
            config_item=config_item,
            sub_items=sub_items,
            filters=filters,
            environment=env,
            id_in_keys=False,
        )

        cmp[env] = items

    print("")

    # create df for each item
    for item in tqdm(cmp.get(environments[0]), desc="Comparing items"):
        tmp_compare = {}
        for env in environments:
            tmp_compare[env] = cmp.get(env).get(item)

        # create dataframe
        df = create_comparison_dataframe(tmp_compare)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)

        # save df
        if not check_all_x_or_nan(df):
            df.to_csv(f"compare/{item}.tsv", sep='\t')

    # display
    print("")
    print(df)
    print("")

    # save JSON file
    with open("compare.json", 'w') as comparison_file:
        json.dump(cmp, comparison_file, indent=4)
        print(f"\nDifferences have been saved to compare/<{config_item}_name>.tsv for your best convenience.")


def create_comparison_dataframe(comparison_dict):
    """
    Create comparison dataframe.

    :param comparison_dict:
    :return:
    """

    # Get environment names
    env_names = list(comparison_dict.keys())

    # Create an empty DataFrame
    df = pd.DataFrame(columns=env_names)

    def process_key_value(prefix, value, env):
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                new_prefix = prefix + '.' + sub_key if prefix else sub_key
                process_key_value(new_prefix, sub_value, env)
        else:
            df.at[prefix, env] = value

    for env in env_names:
        environment_dict = comparison_dict[env]
        process_key_value("", environment_dict, env)

    reference_env = env_names[0]
    for env in env_names[1:]:
        for prefix in df.index:
            reference_value = df.at[prefix, reference_env]
            # replace code otherwise unreadable
            if isinstance(reference_value, str) and (
                    '\r' in reference_value or '\t' in reference_value or '\n' in reference_value):
                df.at[prefix, reference_env] = "<CODE>"
            # check sync
            if df.at[prefix, env] == reference_value:
                df.at[prefix, env] = 'x'
            else:
                if isinstance(df.at[prefix, env], str) and (
                        '\r' in df.at[prefix, env] or '\t' in df.at[prefix, env] or '\n' in df.at[prefix, env]):
                    df.at[prefix, env] = '/!\\'
                if '.import' in prefix:
                    df.at[prefix, env] = '/!\\'
            # replace imports otherwise unreadable
            if '.import' in prefix:
                df.at[prefix, reference_env] = '<IMPORTS>'

    # keys to remove
    keys_to_pop = [r'id', r'objectType', r'externalIds', r'href', r'icons', r'created', r'lastModified',
                   r'visibility', r'owner', r'createdBy', r'account', r'revision', r'createdBy',
                   r'configuration.definition', r'deleted', r'pluginVersion', r'configuration.instance.recipients',
                   r'isExpression', r'description', r'key', r'secret', r'username', r'password', r'url']

    for key in keys_to_pop:
        df = df[~df.index.str.contains(key, regex=True)]

    return df


def check_all_x_or_nan(df):
    """
    Check whether all columns (2+) are 'x' or 'NaN'.

    :param df:
    :return:
    """

    # Select columns 2 or more (0-based index)
    selected_columns = df.iloc[:, 1:]

    # Check if all values in the selected columns are "x" or "NaN"
    return all(selected_columns.apply(lambda col: col.isin(['x', np.nan, None]).all()))
