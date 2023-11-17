#!/usr/bin/python

"""

    PROJECT: flex_toolbox
    FILENAME: toolbox.py
    AUTHOR: David NAISSE
    DATE: September 07, 2023

    DESCRIPTION: terminal command reader
    
"""

import argparse
from distutils.util import strtobool

from VARIABLES import FLEX_ITEMS_PULL, FLEX_ITEMS_LIST, FLEX_ITEMS_PUSH, FLEX_ITEMS_RESTORE, FLEX_ITEMS_COMPARE
from src.compare import compare_command_func
from src.connect import connect_command_func
from src.env import env_command_func
from src.list import list_command_func
from src.pull import pull_command_func
from src.push import push_command_func
from src.query import query_command_func
from src.restore import restore_command_func

if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(description='Flex ToolBoX')
    subparsers = parser.add_subparsers(help='Tools')

    # env
    env_command = subparsers.add_parser('env', help='Show current env')
    env_command.set_defaults(func=env_command_func)

    # connect
    connect_command = subparsers.add_parser('connect', help='Connect to a Flex env')
    connect_command.add_argument('env_url', type=str, help='URL of the Flex environment ')
    connect_command.add_argument('username', type=str, nargs='?', help='Flex username ')
    connect_command.add_argument('password', type=str, nargs='?', help='Flex password ')
    connect_command.set_defaults(func=connect_command_func)

    # list
    list_command = subparsers.add_parser('list', help='List config items from env')
    list_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_LIST, help='Config item to list')
    list_command.add_argument('--filters', type=str, nargs="*", help="Search by text")
    list_command.add_argument('--post_filters', type=str, nargs="*", help="Post retrieval filters")
    list_command.set_defaults(func=list_command_func)

    # # create_action
    # create_action_command = subparsers.add_parser('create_action', help='Create action')
    # create_action_command.add_argument('name', type=str, help='Name of the action')
    # create_action_command.set_defaults(func=create_action_command_func)
    #
    # # create_workflow
    # create_workflow_command = subparsers.add_parser('create_workflow', help='Create workflow')
    # create_workflow_command.add_argument('name', type=str, help='Name of the workflow')
    # create_workflow_command.set_defaults(func=create_workflow_command_func)

    # pull
    pull_command = subparsers.add_parser('pull', help='Pull config items from Flex')
    pull_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_PULL, help='Config item to pull')
    pull_command.add_argument('--filters', type=str, nargs='*', help='Filters to apply')
    pull_command.add_argument('--with_dependencies', type=lambda x: bool(strtobool(x)), help='Whether to retrieve items dependencies', default=True)
    pull_command.add_argument('--post_filters', type=str, nargs="*", help="Post retrieval filters")
    pull_command.set_defaults(func=pull_command_func)

    # push
    push_command = subparsers.add_parser('push', help='Push config items to Flex')
    push_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_PUSH, help='Config item to push')
    push_command.add_argument('item_names', type=str, nargs='*', help='Items to push')
    push_command.add_argument('--push_to_failed_jobs', type=bool, default=False)
    # push_command.add_argument('--all', type=bool, help='Whether to push all config items or not')
    push_command.set_defaults(func=push_command_func)

    # restore
    restore_command = subparsers.add_parser('restore', help='Restore config items')
    restore_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_RESTORE, help='Config item to restore')
    restore_command.add_argument('item_name', type=str, help='Item to restore')
    restore_command.add_argument('backup', type=str, help='Backup to restore')
    restore_command.set_defaults(func=restore_command_func)

    # query
    query_command = subparsers.add_parser('query', help='Query API')
    query_command.add_argument('method', type=str, choices=['GET', 'POST', 'PUT'], default='GET')
    query_command.add_argument('url', type=str, help='Query to send')
    query_command.add_argument('--payload', type=str, help='File to use as payload')
    query_command.set_defaults(func=query_command_func)

    # compare
    compare_command = subparsers.add_parser('compare', help='Compare a config item against several environments')
    compare_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_COMPARE, help='Config item to compare')
    compare_command.add_argument('environments', type=str, nargs='*', help='Environments')
    compare_command.add_argument('--filters', type=str, nargs='*', help='Filters to apply')
    compare_command.set_defaults(func=compare_command_func)

    # todo:
    #     env in command
    #     cancel
    #     sync

    args = parser.parse_args()
    args.func(args)
