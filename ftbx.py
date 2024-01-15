#!/usr/bin/python3

"""

    PROJECT: flex_toolbox
    FILENAME: toolbox.py
    AUTHOR: David NAISSE
    DATE: September 07, 2023

    DESCRIPTION: terminal command reader

"""

import argparse

from VARIABLES import FLEX_ITEMS_PULL, FLEX_ITEMS_LIST, FLEX_ITEMS_PUSH, FLEX_ITEMS_RESTORE, FLEX_ITEMS_COMPARE, \
    FLEX_ITEMS_RETRY, FLEX_ITEMS_LAUNCH
from src.compare import compare_command_func
from src.connect import connect_command_func
from src.env import env_command_func
from src.init import init_command_func
from src.launch import launch_command_func
from src.list import list_command_func
from src.pull import pull_command_func
from src.push import push_command_func
from src.query import query_command_func
from src.restore import restore_command_func
from src.retry import retry_command_func

if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(description='Flex ToolBoX')
    subparsers = parser.add_subparsers(help='Tools')

    # init
    init_command = subparsers.add_parser('init', help='Initialize Flex ToolBox (multi-OS)')
    init_command.set_defaults(func=init_command_func)

    # env
    env_command = subparsers.add_parser('env', help='Show available environments and default environment')
    env_command.set_defaults(func=env_command_func)

    # connect
    connect_command = subparsers.add_parser('connect', help='Connect to a Flex env (url, username, pwd)')
    connect_command.add_argument('env_url', type=str, help='URL of the Flex environment')
    connect_command.add_argument('username', type=str, nargs='?', help='Flex username')
    connect_command.add_argument('password', type=str, nargs='?', help='Flex password')
    connect_command.add_argument('--alias', type=str, nargs='?', help='Env alias')
    connect_command.set_defaults(func=connect_command_func)

    # list
    list_command = subparsers.add_parser('list', help='List (to CSV & JSON) config items from an environment, with filters and post-filters')
    list_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_LIST, help='Config item to list')
    list_command.add_argument('--filters', type=str, nargs="*", help="Search by text")
    list_command.add_argument('--post-filters', dest="post_filters", type=str, nargs="*", help="Post retrieval filters")
    list_command.add_argument('--from', dest="from_", type=str, help="Environment to list items from", default="default")
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
    pull_command = subparsers.add_parser('pull', help='Pull (files & folders) config items from an environment, with filters and post-filters')
    pull_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_PULL, help='Config item to pull')
    pull_command.add_argument('--filters', type=str, nargs='*', help='Filters to apply')
    pull_command.add_argument('--with-dependencies', dest="with_dependencies", action='store_true', help='Whether to retrieve items dependencies')
    pull_command.add_argument('--post-filters', dest="post_filters", type=str, nargs="*", help="Post retrieval filters")
    pull_command.add_argument('--from', dest="from_", type=str, nargs="*", help="Environments to pull items from")
    pull_command.set_defaults(func=pull_command_func)

    # push
    push_command = subparsers.add_parser('push', help='Push (create or update) config items to an environment')
    push_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_PUSH, help='Config item to push')
    push_command.add_argument('item_names', type=str, nargs='*', help='Items to push')
    push_command.add_argument('--from', dest="from_", type=str, default="default", help='Environment to push from')
    push_command.add_argument('--to', type=str, nargs='*', default=["default"], help='Environments to push to')
    push_command.add_argument('--push-to-failed-jobs', nargs='?', const=True, default=False, help='Whether to retry failed jobs with new code. If a value is provided, it will be treated as the filename.')
    # push_command.add_argument('--all', type=bool, help='Whether to push all config items or not')
    # todo: --retry
    # todo: same syntax than pull
    push_command.set_defaults(func=push_command_func)

    # restore
    # todo: env
    restore_command = subparsers.add_parser('restore', help='Restore config items to a previous point in time')
    restore_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_RESTORE, help='Config item to restore')
    restore_command.add_argument('item_name', type=str, help='Item to restore')
    restore_command.add_argument('backup', type=str, help='Backup to restore')
    restore_command.set_defaults(func=restore_command_func)

    # query
    query_command = subparsers.add_parser('query', help='Query (GET, POST, PUT) an environment with or without payload (file or command line arguments)')
    query_command.add_argument('method', type=str, choices=['GET', 'POST', 'PUT'], default='GET')
    query_command.add_argument('url', type=str, help='Query to send')
    query_command.add_argument('--from', dest="from_", type=str, help='Environment to query', default="default")
    query_command.add_argument('--payload', type=str, nargs='*', help='File or arguments to use as payload')
    query_command.set_defaults(func=query_command_func)

    # compare
    compare_command = subparsers.add_parser('compare', help='Compare config items against several environments')
    compare_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_COMPARE, help='Config item to compare')
    compare_command.add_argument('environments', type=str, nargs='*', help='Environments')
    compare_command.add_argument('--filters', type=str, nargs='*', help='Filters to apply')
    compare_command.set_defaults(func=compare_command_func)

    # retry
    retry_command = subparsers.add_parser('retry', help='Retry or bulk retry config item instances within an environment')
    retry_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_RETRY, help='Config item')
    retry_command.add_argument('--from', dest="from_", type=str, default="default", help='Environment to retry from')
    retry_command.add_argument('--filters', type=str, nargs='*', default=[], help='Filters to apply')
    retry_command.add_argument('--file', type=str, default=None, help='File containing items to retry')
    retry_command.set_defaults(func=retry_command_func)

    # launch
    launch_command = subparsers.add_parser('launch', help='Launch a config item instance within an environment')
    launch_command.add_argument('config_item', type=str, choices=FLEX_ITEMS_LAUNCH, help='Config item to launch')
    launch_command.add_argument('item_name', type=str, help='Item name')
    launch_command.add_argument('--in', dest="in_", type=str, default="default", help='Environment to launch instance in')
    launch_command.add_argument('--params', type=str, nargs='*', default=[], help='Parameters to use')
    launch_command.add_argument('--from-file', type=str, help='Parameters file to use')
    launch_command.add_argument('--use-local', nargs='?', const=True, default=False, help='Whether to push local config to remote before launching an instance')
    launch_command.set_defaults(func=launch_command_func)

    # todo:
    #     push with rename should delete old local file
    #     create items from CSV
    #     logs and log file
    #     push workflows + their scripts
    #     cancel
    #     sync
    #     major speedup required for get_items with threads
    #     listen

    args = parser.parse_args()
    args.func(args)
