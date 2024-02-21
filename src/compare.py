"""

    PROJECT: flex_toolbox
    FILENAME: compare.py
    AUTHOR: David NAISSE
    DATE: October 17, 2023

    DESCRIPTION: compare command functions

    TEST STATUS: FULLY TESTED
"""
import os

import pandas as pd
from tqdm import tqdm

from src.utils import get_items, create_folder, enumerate_sub_items


def compare_command_func(args):
    """
    Action on compare command.

    TEST STATUS: FULLY TESTED
    """

    if len(args.environments) >= 2:

        # compare items
        compare_items(config_item=args.config_item, environments=args.environments, filters=args.filters,
                      sub_items=enumerate_sub_items(config_item=args.config_item))

    else:
        print(f"Cannot compare {args.config_item} if number of environments provided is less than 2 "
              f"(provided: {args.environments}). ")


def compare_items(config_item: str, filters: list, environments: list, sub_items: list = []):
    """
    Compare items between environments.

    TEST STATUS: DOES NOT REQUIRE TESTING

    :param sub_items: sub items
    :param config_item: config item (ex: actions, workflowDefinitions)
    :param filters: filters to apply
    :param environments: envs (ex: customer-dev, customer-stg, customer-prod)
    :return:
    """

    cmp = {}

    # create comparison folders
    create_folder(folder_name=f"compare_{'_'.join(environments)}", ignore_error=True)
    create_folder(folder_name=os.path.join(f"compare_{'_'.join(environments)}", config_item), ignore_error=True)

    # get item from envs
    for env in environments:
        items = get_items(
            config_item=config_item,
            filters=filters,
            sub_items=sub_items,
            environment=env,
            id_in_keys=False,
        )

        cmp[env] = items

    print("")

    # create diff df for each item
    for item in tqdm(cmp.get(environments[0]), desc=f"Comparing items between {environments}"):
        tmp_compare = {}

        # flatten dicts
        for env in environments:
            tmp_compare[env] = flatten_dict(cmp.get(env).get(item, {}))

        # compare
        result = compare_dicts_list(dict_list=[d for d in tmp_compare.values()], environments=environments)

        # save
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)
        if result is not None: result.to_csv(os.path.join(f"compare_{'_'.join(environments)}", config_item, f"{item}.tsv"), sep="\t")

    print("\nResult of the comparison (if there are any differences) have been saved in "
          f"compare_{'_'.join(environments)}/{config_item}/<item_name>.tsv for your best convenience. \n")


def flatten_dict(input_dict, parent_key='', sep='.'):
    """
    Flatten a nested dict recursively to get a dict with one key per nested item.*

    TEST STATUS: TODO

    :param input_dict: input dictionary
    :param parent_key: parent key (or subdict) to flatten
    :param sep: separator between keys
    """

    flattened_dict = {}

    # for each k/v
    for k, v in input_dict.items():
        # get current key path
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        # handle item type
        # if item is dict, flatten subdict
        if isinstance(v, dict):
            flattened_dict.update(flatten_dict(v, new_key, sep=sep))
        # if item is list, flatten each item in the list
        elif isinstance(v, list):
            for i, list_item in enumerate(v):
                if isinstance(list_item, dict):
                    flattened_dict.update(flatten_dict(list_item, f"{new_key}.{'{:05d}'.format(i)}", sep=sep))
                else:
                    flattened_dict[f"{new_key}.{'{:05d}'.format(i)}"] = v

        # neither list nor dict, add to flattened dict
        else:
            if isinstance(v, str) and "\n" in v:
                multiline = v.replace("\t", "").split('\n')
                for idx, line in enumerate(multiline):
                    flattened_dict[f"{new_key}{sep}line{'{:05d}'.format(idx)}"] = line.strip()
            else:
                flattened_dict[new_key] = v

    return flattened_dict


def compare_dicts_list(dict_list, environments: list, exclude_keys=None):
    """
    Compare a list of flattened dicts and returns a dataframe containing only differences.

    TEST STATUS: TODO

    :param dict_list: list of flattened dicts
    :param environments: list of environments
    :param exclude_keys: keys to exclude from returned dataframe (contain-type match)
    """

    # check dict_list is a list of dict
    if not dict_list or not all(isinstance(d, dict) for d in dict_list):
        raise ValueError("Input should be a non-empty list of dictionaries.")

    # keys that are removed by default
    if exclude_keys is None:
        exclude_keys = [
            r'id',
            r'Id',
            r'assignment',
            r'objectType',
            r'externalIds',
            r'href',
            r'icons',
            r'created',
            r'lastModified',
            r'visibility',
            r'owner',
            r'createdBy',
            r'account.',
            r'revision',
            r'deleted',
            r'latestVersion',
            r'plugin',
            r'configuration.instance.recipients',
            r'isExpression',
            r'description',
            r'secret',
            r'properties.message',
            r'username',
            r'password',
            r'structure',
            r'url',
            r'metadata.definition',
            r'saml-configuration',
            r'external-authentication-workspace',
            r'external-authentication-endpoint',
            r'configuration.definition'
        ]

    # make a set of all unique keys found in all flattened dicts
    unique_keys = set()
    for d in dict_list:
        unique_keys.update(d.keys())

    # for each key in the unique keys set, compare the values between flattened dicts
    comparison_data = {}
    for key in unique_keys:
        # exclude useless keys
        if any(exclude_key in key for exclude_key in exclude_keys):
            continue

        # compare values between flattened dict
        values = [d.get(key) for d in dict_list]
        if len(set(values)) > 1:
            comparison_data[key] = values

    # make it a dataframe
    diff_df = pd.DataFrame(comparison_data)
    diff_df = diff_df.transpose()
    diff_df = diff_df.sort_index()
    try:
        diff_df.columns = [e for e in environments]
    except Exception as ex:
        # here means no differences
        if "Expected axis has 0 elements" in str(ex):
            diff_df = None
        else:
            raise Exception(ex)

    return diff_df
