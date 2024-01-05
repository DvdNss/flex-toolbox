"""

    PROJECT: flex_toolbox
    FILENAME: restore.py
    AUTHOR: David NAISSE
    DATE: October 05, 2023

    DESCRIPTION: restore command functions

    TEST STATUS: DOES NOT REQUIRE TESTING
"""
import json
import os

from src.push import push_item


def restore_command_func(args):
    """
    Action on restore command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    # if path exists
    if os.path.isdir(f"{args.config_item}/{args.item_name}/backup/{args.backup}"):

        # check if is action
        with open(f"{args.config_item}/{args.item_name}/backup/{args.backup}/_object.json", 'r') as config_file:
            data = json.load(config_file)

        if args.config_item == 'actions' and data['objectType']['name'] == 'action':
            push_item(config_item=args.config_item, item_name=args.item_name, item_config=data, restore=True)
        else:
            print(f'Cannot restore backup {args.item}/backup/{args.backup} since it is not an action.\n')

    # path doesn't exist
    else:
        print(f"Cannot find folder for {args.item}/backup/{args.backup}.\n")
