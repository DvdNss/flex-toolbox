"""

    PROJECT: flex_toolbox
    FILENAME: retry.py
    AUTHOR: David NAISSE
    DATE: December 12, 2023

    DESCRIPTION: retry command functions
    
"""
import json

import pandas as pd
from tqdm import tqdm

from src.env import get_default_env_alias
from src.utils import get_items, retry_config_item_instance, get_auth_material


def retry_command_func(args):
    """Action on retry command. """

    retried_instances = pd.DataFrame(columns=['config_item', 'name', 'id', 'status', 'progress'])

    # default env alias
    environment = get_default_env_alias() if args.from_ == 'default' else args.from_
    env, auth = get_auth_material(environment=environment)

    # add specific filters
    args.filters.append("status=Failed")

    # input is file
    if args.file:

        # csv
        if ".csv" in args.file:
            df = pd.read_csv(args.file)

            print(f"\nPerforming [POST] {env['url']}/api/{args.config_item}/<ids>/actions...\n")

            # iterate over df and retry instances
            for id in tqdm(df['id'], desc=f"Retrying {args.config_item}"):
                name, progress = retry_config_item_instance(config_item=args.config_item, id=id,
                                                            environment=environment)
                retried_instances.loc[len(retried_instances) + 1] = {
                    'config_item': args.config_item,
                    'name': name,
                    'id': id,
                    'status': "Running",
                    'progress': str(progress) + "%",
                }

        # json
        elif ".json" in args.file:
            with open(args.file, "r") as json_file:
                items = json.load(json_file)

            print(f"\nPerforming [POST] {env['url']}/api/{args.config_item}/<ids>/actions...\n")

            # iterate over keys and retry instances
            for instance, instance_config in tqdm(items.items(), desc=f"Retrying {args.config_item}"):
                name, progress = retry_config_item_instance(
                    config_item=args.config_item,
                    id=instance_config.get('id'),
                    environment=environment
                )
                retried_instances.loc[len(retried_instances) + 1] = {
                    'config_item': args.config_item,
                    'name': name,
                    'id': instance_config.get('id'),
                    'status': "Running",
                    'progress': str(progress) + "%",
                }

        else:
            print(
                f"Sorry, {args.file} doesn't belong to the supported formats. Please try with .JSON or .CSV instead. ")
    # input is filters
    else:

        # retrieve failed items
        failed_items = get_items(
            config_item=args.config_item,
            filters=args.filters,
            environment=environment,
            log=True
        )

        # retry instances
        for failed_item, failed_item_config in tqdm(failed_items.items(), desc=f"Retrying {args.config_item}"):
            name, progress = retry_config_item_instance(
                config_item=args.config_item,
                id=failed_item_config.get('id'),
                environment=environment
            )
            retried_instances.loc[len(retried_instances) + 1] = {
                'config_item': args.config_item,
                'name': name,
                'id': failed_item_config.get('id'),
                'status': "Running",
                'progress': str(progress) + "%",
            }

    print(f"\nAll {args.config_item} have been retried successfully in {environment}. List of retried items can "
          f"be found in retried_instances.csv. First 25 instances are shown below. \n")

    # save and log
    retried_instances.index = range(1, len(retried_instances) + 1)
    pd.set_option('display.colheader_justify', 'center')
    retried_instances.to_csv(path_or_buf="retried_instances.csv", sep=",")
    print(retried_instances.head(25), '\n')
