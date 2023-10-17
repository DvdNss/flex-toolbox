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

from src.utils import get_items


def compare_command_func(args):
    """Action on pull command. """

    if len(args.environments) >= 2:
        compare_items(config_item=args.config_item, item_name=args.item_name, environments=args.environments)
    else:
        print(
            f"Cannot compare {args.config_item} if number of environments provided is less than 2 (provided: {args.environments}). ")


def compare_items(config_item: str, item_name: str, environments: list, local: bool = False, sub_items: list = []):
    """
    Compare items between environments.

    :param sub_items: sub items
    :param local: whether to use local comparison or not
    :param config_item: config item (ex: actions, workflowDefinitions)
    :param item_name: item name (ex: update-asset-metadata)
    :param environments: envs (ex: customer-dev, customer-stg, customer-prod)
    :return:
    """

    cmp = {}

    keys_to_pop = ['id', 'uuid', 'objectType', 'externalIds', 'href', 'type', 'icons', 'created', 'lastModified',
                   'visibility', 'owner', 'createdBy', 'account', 'revision']

    # get item from envs
    for env in environments:
        item = get_items(
            config_item=config_item,
            sub_items=sub_items,
            filters=[f"name={item_name}", 'exactNameMatch=true', 'limit=1'],
            environment=env
        )

        # from depth = 2 to depth =1
        item = item[list(item.keys())[0]]

        # pluginClass is very long, so shortening it
        try:
            item['pluginClass'] = item['pluginClass'].split(".")[-1]
        except:
            pass

        # pop useless keys
        for key_to_pop in keys_to_pop:
            try:
                item.pop(key_to_pop)
            except:
                pass

        cmp[env] = item

    # create dataframe
    df = create_comparison_dataframe(cmp)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

    # display
    print("")
    print(df)
    print("")

    # save JSON file
    with open("compare.json", 'w') as comparison_file:
        json.dump(cmp, comparison_file, indent=4)


def create_comparison_dataframe(comparison_dict):
    """
    Create comparison dataframe

    :param comparison_dict:
    :return:
    """

    # get environment names
    env_names = list(comparison_dict.keys())

    # create empty DataFrame
    df = pd.DataFrame(columns=env_names)

    # iterate through keys in the reference environment
    reference_env = env_names[0]
    for key, value in comparison_dict[reference_env].items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                df.at[key + '.' + sub_key, reference_env] = sub_value
        else:
            df.at[key, reference_env] = value

    # iterate through non-reference environment
    for env in env_names[1:]:
        for key, value in comparison_dict[env].items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if key in comparison_dict[reference_env] and sub_key in comparison_dict[reference_env][key]:
                        reference_value = comparison_dict[reference_env].get(key, {}).get(sub_key)
                    else:
                        reference_value = np.nan
                    if sub_value != reference_value:
                        df.at[key + '.' + sub_key, env] = sub_value
                    else:
                        df.at[key + '.' + sub_key, env] = 'NULL'
            else:
                reference_value = comparison_dict[reference_env].get(key)
                if value != reference_value:
                    df.at[key, env] = value
                else:
                    df.at[key, env] = 'x'

    return df
