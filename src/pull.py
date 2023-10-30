"""

    PROJECT: flex_toolbox
    FILENAME: pull.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: pull command functions
    
"""
import json

from src.utils import create_folder, get_tags_and_taxonomies, get_items, get_taxonomies, get_full_items, save_items, \
    save_taxonomies


def pull_command_func(args):
    """Action on pull command. """

    if args.config_item != "all":
        get_full_items(config_item=args.config_item, filters=args.filters, post_filters=args.post_filters, save=True)
    else:
        pull_all()


def pull_all() -> bool:
    """
    Pull all.

    :return: True if succeeds, False if fails
    """

    # accounts
    sorted_items = get_items(config_item="accounts", sub_items=['configuration', 'properties'],
                             filters=['enabled=true'])
    save_items(config_item='accounts', items=sorted_items)
    print('---')
    # actions
    sorted_items = get_items(config_item='actions', sub_items=['configuration'], filters=['enabled=true'])
    save_items(config_item='actions', items=sorted_items)
    print('---')
    # collections
    sorted_items = get_items(config_item='collections', sub_items=['metadata'])
    save_items(config_item='collections', items=sorted_items)
    print('---')
    # event Handlers
    sorted_items = get_items(config_item='eventHandlers', sub_items=['configuration'], filters=['enabled=true'])
    save_items(config_item='eventHandlers', items=sorted_items)
    print('---')
    # groups
    sorted_items = get_items(config_item='groups', sub_items=['members'], filters=['enabled=true'])
    save_items(config_item='groups', items=sorted_items)
    print('---')
    # message Templates
    sorted_items = get_items(config_item='messageTemplates', sub_items=['body'], filters=['enabled=true'])
    save_items(config_item='messageTemplates', items=sorted_items)
    print('---')
    # metadata Definitions
    sorted_items = get_items(config_item='metadataDefinitions', sub_items=['definition'], filters=['enabled=true'])
    save_items(config_item='metadataDefinitions', items=sorted_items)
    print('---')
    # object Types
    sorted_items = get_items(config_item='objectTypes', sub_items=[])
    save_items(config_item='objectTypes', items=sorted_items)
    print('---')
    # profiles
    sorted_items = get_items(config_item='profiles', sub_items=['configuration'], filters=['enabled=true'])
    save_items(config_item='profiles', items=sorted_items)
    print('---')
    # quotas
    sorted_items = get_items(config_item='quotas', sub_items=[], filters=['enabled=true'])
    save_items(config_item='quotas', items=sorted_items)
    print('---')
    # resources
    sorted_items = get_items(config_item='resources', sub_items=['configuration'], filters=['enabled=true'])
    save_items(config_item='resources', items=sorted_items)
    print('---')
    # roles
    sorted_items = get_items(config_item='roles', sub_items=[])
    save_items(config_item='roles', items=sorted_items)
    print('---')
    # tag Collections
    # no way to retrieve tags from API directly, so bypassing by reading tags from MD DEFs
    # NOTE: Will only retrieve tags that are used by MD DEFs
    print("\nRetrieving tagCollections from Metadata Definitions as "
          "it is not possible to list them directly from the API...\nPlease note that only tagCollections that are used"
          " in metadata definitions will be retrieved.")
    metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
    sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['tagCollections'])
    save_items(config_item='tagCollections', items=sorted_items)
    print('---')
    # task Definitions
    sorted_items = get_items(config_item='taskDefinitions', sub_items=[])
    save_items(config_item='taskDefinitions', items=sorted_items)
    print('---')
    # taxonomies
    sorted_items = get_taxonomies(filters=['enabled=true'])
    save_taxonomies(taxonomies=sorted_items)
    print('---')
    # timed Actions
    sorted_items = get_items(config_item='timedActions', sub_items=['configuration'])
    save_items(config_item='timedActions', items=sorted_items)
    print('---')
    # user defined object types
    sorted_items = get_items(config_item='userDefinedObjectTypes', sub_items=['hierarchy', 'relationships'])
    save_items(config_item='userDefinedObjectTypes', items=sorted_items)
    print('---')
    # variants
    sorted_items = get_items(config_item='variants', sub_items=[])
    save_items(config_item='variants', items=sorted_items)
    print('---')
    # wizards
    sorted_items = get_items(config_item='wizards', sub_items=['configuration'], filters=['enabled=true'])
    save_items(config_item='wizards', items=sorted_items)
    print('---')
    # workflow Definitions
    sorted_items = get_items(config_item='workflowDefinitions', sub_items=['structure'], filters=['enabled=true'])
    save_items(config_item='workflowDefinitions', items=sorted_items)
    print('---')
    # workspaces
    sorted_items = get_items(config_item='workspaces', sub_items=[], filters=['enabled=true'])
    save_items(config_item='workspaces', items=sorted_items)

    return True
