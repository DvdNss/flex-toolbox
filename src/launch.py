"""

    PROJECT: flex_toolbox
    FILENAME: launch.py
    AUTHOR: David NAISSE
    DATE: December 21, 2023

    DESCRIPTION: Launch command functions

    TEST STATUS: FULLY TESTED
"""
import json
import os

from src.env import get_default_env_alias
from src.push import push_item
from src.utils import get_items, launch_config_item_instance


def launch_command_func(args):
    """
    Action on launch command.

    TEST STATUS: FULLY TESTED
    """

    instance_to_config_item_map = {
        'jobs': 'actions',
        'workflows': 'workflowDefinitions',
    }

    payload = {}

    # check that config instance exists
    config_item = instance_to_config_item_map.get(args.config_item)
    item = get_items(config_item=config_item, filters=['exactNameMatch=true', f'name={args.item_name}'],
                     environment=args.in_, log=False)
    try:
        item = item.get(list(item)[0])
    except:
        print(f"\nCould not find item {config_item}:{args.item_name} in {args.in_}. "
              f"Please check that the information provided is correct and try again.\n")
        quit()

    # make sure we got the correct one
    assert item.get('name') == args.item_name, \
        f"\nRetrieved item {config_item}:{item.get('name')} does not match input item {config_item}:{args.item_name}.\n"

    # set main payload param
    payload['actionId' if config_item == 'actions' else 'definitionId'] = item.get('id')

    # arg params or file params
    if args.from_file and not args.params:
        # read params from json
        if ".json" in args.from_file:
            with open(args.from_file) as launch_config_file:
                tmp_payload = json.load(launch_config_file)
                # remove actionId and definitionId since we already have this info
                for key, value in tmp_payload.items():
                    if key != 'actionId' and key != 'definitionId':
                        payload[key] = value
        else:
            print(f"\nFile {args.from_file} is not supported. Please use a JSON file instead.\n")
            quit()
    # read params from args
    elif args.params and not args.from_file:
        for param in args.params:
            key, value = param.split('=')[0], param.split('=')[1]
            # remove actionId and definitionId since we already have this info
            if key != 'actionId' and key != 'definitionId':
                payload[key] = value

    # handle --use-local
    if args.use_local:
        # get default env alias if not specified in args
        environment = get_default_env_alias() if args.in_ == 'default' else args.in_
        # assert local config exists
        if os.path.isdir(os.path.join(environment, config_item, item.get('name'))):
            # get obj
            with open(os.path.join(environment, config_item, item.get('name'), '_object.json'), 'r') as config_file:
                data = json.load(config_file)
            # push
            push_item(
                config_item=config_item,
                item_name=item.get('name'),
                item_config=data,
                src_environment=environment,
                dest_environment=environment,
                log=False
            )
        else:
            print(f"\nCannot find {environment}/{config_item}/{item.get('name')}. "
                  f"Please check that the information provided is correct and try again.\n")
            quit()

    # launch instance
    instance = launch_config_item_instance(config_item=args.config_item, payload=payload, environment=args.in_)
    print(
        f"Instance ID {instance.get('id')} [{args.config_item[:-1]}:{instance.get('name')}] has been launched successfully.\n ")

    return instance
