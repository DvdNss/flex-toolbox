"""

    PROJECT: flex_toolbox
    FILENAME: pull.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: pull command functions
    
"""
import json
from typing import List

import requests

from src.utils import create_folder, get_tags_and_taxonomies, get_items, get_taxonomies, get_surrounding_items

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def pull_command_func(args):
    """Action on pull command. """

    if args.config_item != "all":
        pull_items(config_item=args.config_item, filters=args.filters)
    else:
        pull_all()


def save_items(config_item: str, items: dict):
    """
    Save Flex items to JSON

    :param config_item: config item
    :param items: dict of items
    :return:
    """

    # parent folder
    create_folder(folder_name=config_item, ignore_error=True)

    print("")

    # folder for each config
    for item in items:

        # folder's name
        if config_item == 'events':
            folder_name = f"{items.get(item).get('id')}"
        elif config_item == 'jobs' or config_item == 'tasks' or config_item == 'workflows':
            folder_name = f"{items.get(item).get('id')}".replace("/", "").replace(":", "")
        else:
            folder_name = f"{items.get(item).get('name')}".replace("/", "").replace(":", "")

        # create object folder
        create_folder(folder_name=f"{config_item}/{folder_name}", ignore_error=True)

        # save subfields in other files
        if 'configuration' in items.get(item) and items.get(item).get('configuration').get('instance'):
            # if groovy script
            if 'script-contents' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=f"{config_item}/{folder_name}", item_config=items.get(item))
            elif 'internal-script' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=f"{config_item}/{folder_name}", item_config=items.get(item))
            elif 'script_type' in items.get(item).get('configuration').get('instance'):
                create_script(item_name=f"{config_item}/{folder_name}", item_config=items.get(item))
            else:
                with open(f"{config_item}/{folder_name}/configuration.json", "w") as item_config:
                    json.dump(obj=items.get(item).get('configuration').get('instance'), fp=item_config, indent=4)
                    items.get(item).pop('configuration')

        if 'asset' in items.get(item) and items.get(item).get('asset'):
            with open(f"{config_item}/{folder_name}/asset.json", "w") as item_config:
                json.dump(obj=items.get(item).get('asset'), fp=item_config, indent=4)
                items.get(item).pop('asset')

        if 'workflowInstance' in items.get(item) and items.get(item).get('workflowInstance'):
            with open(f"{config_item}/{folder_name}/workflowInstance.json", "w") as item_config:
                json.dump(obj=items.get(item).get('workflowInstance'), fp=item_config, indent=4)
                items.get(item).pop('workflowInstance')

        if 'definition' in items.get(item) and items.get(item).get('definition').get('definition'):
            with open(f"{config_item}/{folder_name}/definition.json", "w") as item_config:
                json.dump(obj=items.get(item).get('definition').get('definition'), fp=item_config, indent=4)
                items.get(item).pop('definition')

        if 'body' in items.get(item) and items.get(item).get('body'):
            with open(f"{config_item}/{folder_name}/body.txt", "w") as item_config:
                item_config.write(items.get(item).get('body'))
                items.get(item).pop('body')

        if 'workflow' in items.get(item) and items.get(item).get('workflow'):
            with open(f"{config_item}/{folder_name}/workflow.json", "w") as item_config:
                json.dump(obj=items.get(item).get('workflow'), fp=item_config, indent=4)
                items.get(item).pop('workflow')

        if 'properties' in items.get(item) and items.get(item).get('properties').get('accountProperties'):
            with open(f"{config_item}/{folder_name}/properties.json", "w") as item_config:
                json.dump(obj=items.get(item).get('properties').get('accountProperties'), fp=item_config, indent=4)
                items.get(item).pop('properties')

        if 'references' in items.get(item) and items.get(item).get('references').get('objects'):
            with open(f"{config_item}/{folder_name}/references.json", "w") as item_config:
                json.dump(obj=items.get(item).get('references').get('objects'), fp=item_config, indent=4)
                items.get(item).pop('references')

        if 'metadata' in items.get(item) and items.get(item).get('metadata').get('instance'):
            with open(f"{config_item}/{folder_name}/metadata.json", "w") as item_config:
                json.dump(obj=items.get(item).get('metadata').get('instance'), fp=item_config, indent=4)
                items.get(item).pop('metadata')

        if 'fileInformation' in items.get(item) and items.get(item).get('fileInformation'):
            with open(f"{config_item}/{folder_name}/fileInformation.json", "w") as item_config:
                json.dump(obj=items.get(item).get('fileInformation'), fp=item_config, indent=4)
                items.get(item).pop('fileInformation')

        if 'assetContext' in items.get(item) and items.get(item).get('assetContext'):
            with open(f"{config_item}/{folder_name}/assetContext.json", "w") as item_config:
                json.dump(obj=items.get(item).get('assetContext'), fp=item_config, indent=4)
                items.get(item).pop('assetContext')

        if 'members' in items.get(item) and items.get(item).get('members').get('users'):
            with open(f"{config_item}/{folder_name}/members.json", "w") as item_config:
                json.dump(obj=items.get(item).get('members').get('users'), fp=item_config, indent=4)
                items.get(item).pop('members')

        if 'role' in items.get(item) and items.get(item).get('role'):
            with open(f"{config_item}/{folder_name}/role.json", "w") as item_config:
                json.dump(obj=items.get(item).get('role'), fp=item_config, indent=4)
                items.get(item).pop('role')

        if 'permissions' in items.get(item) and items.get(item).get('permissions'):
            with open(f"{config_item}/{folder_name}/permissions.json", "w") as item_config:
                json.dump(obj=items.get(item).get('permissions'), fp=item_config, indent=4)
                items.get(item).pop('permissions')

        if 'hierarchy' in items.get(item) and items.get(item).get('hierarchy'):
            with open(f"{config_item}/{folder_name}/hierarchy.json", "w") as item_config:
                json.dump(obj=items.get(item).get('hierarchy'), fp=item_config, indent=4)
                items.get(item).pop('hierarchy')

        if 'structure' in items.get(item) and items.get(item).get('structure'):
            with open(f"{config_item}/{folder_name}/structure.json", "w") as item_config:
                json.dump(obj=items.get(item).get('structure'), fp=item_config, indent=4)
                items.get(item).pop('structure')

        if 'variables' in items.get(item) and items.get(item).get('variables'):
            with open(f"{config_item}/{folder_name}/variables.json", "w") as item_config:
                json.dump(obj=items.get(item).get('variables'), fp=item_config, indent=4)
                items.get(item).pop('variables')

        if 'jobs' in items.get(item) and items.get(item).get('jobs').get('jobs'):
            with open(f"{config_item}/{folder_name}/jobs.json", "w") as item_config:
                json.dump(obj=items.get(item).get('jobs').get('jobs'), fp=item_config, indent=4)
                items.get(item).pop('jobs')

        if 'history' in items.get(item) and items.get(item).get('history'):
            history = items.get(item).get('history').copy()
            for idx, logs in enumerate(history.get('events')):
                history.get('events')[idx].pop('object')
                history.get('events')[idx].pop('user')
            with open(f"{config_item}/{folder_name}/history.json", "w") as item_config:
                json.dump(obj=items.get(item).get('history'), fp=item_config, indent=4)
                items.get(item).pop('history')

        try:
            if 'relationships' in items.get(item) and items.get(item).get('relationships').get('relationships'):
                with open(f"{config_item}/{folder_name}/relationships.json", "w") as item_config:
                    json.dump(obj=items.get(item).get('relationships').get('relationships'), fp=item_config, indent=4)
                    items.get(item).pop('relationships')
        except:
            pass

        # save main object
        with open(f"{config_item}/{folder_name}/_object.json", "w") as item_config:
            json.dump(obj=items.get(item), fp=item_config, indent=4)
            print(f"{config_item}: {folder_name} has been retrieved successfully. ")

    print("") if items else None


def save_taxonomies(taxonomies):
    """
    Save taxonomies.

    :param taxonomies:
    :return:
    """

    # create parent folder
    create_folder(folder_name="taxonomies", ignore_error=True)

    print("")

    for idx, taxonomy in enumerate(taxonomies):
        # create taxonomy folder
        create_folder(folder_name=f"taxonomies/{taxonomy.get('name')}", ignore_error=True)

        # save taxonomy
        with open(f"taxonomies/{taxonomy.get('name')}/_object.json", "w") as item_config:
            json.dump(obj=taxonomies[idx], fp=item_config, indent=4)
            print(f"taxonomies: {taxonomy.get('name')} has been retrieved successfully. ")

    print("") if taxonomies else None


def pull_items(config_item: str, filters: List[str] = []) -> bool:
    """
    List items ids.

    :param config_item: item to retrieve from API (ex: workflows, accounts..)
    :param filters: filters to apply

    :return: True if succeeds, False if fails
    """

    if config_item == 'accounts':
        sorted_items = get_items(config_item=config_item, sub_items=['metadata', 'properties'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'actions':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'assets':
        sorted_items = get_items(config_item=config_item, sub_items=['metadata'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'collections':
        sorted_items = get_items(config_item=config_item, sub_items=['metadata'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'eventHandlers':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'events':
        sorted_items = get_items(config_item=config_item, filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'groups':
        sorted_items = get_items(config_item=config_item, sub_items=['members'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'jobs':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration', 'history'], filters=filters)
        sorted_items = get_surrounding_items(config_item=config_item, items=sorted_items,
                                             sub_items=['asset', 'workflow'])
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'messageTemplates':
        sorted_items = get_items(config_item=config_item, sub_items=['body'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'metadataDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=['definition'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'objectTypes':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'profiles':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'quotas':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'resources':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'roles':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'tagCollections':
        # no way to retrieve tags from API directly, so bypassing by reading tags from MD DEFs
        # NOTE: Will only retrieve tags that are used by MD DEFs
        print("\nRetrieving tagCollections from Metadata Definitions as "
              "it is not possible to list them directly from the API...\nPlease note that only tagCollections that are used"
              " in metadata definitions will be retrieved.")
        metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
        sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['tagCollections'])
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'taskDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'tasks':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'taxonomies':
        taxonomies = get_taxonomies(filters=filters)
        save_taxonomies(taxonomies=taxonomies)
    elif config_item == 'timedActions':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'userDefinedObjectTypes':
        sorted_items = get_items(config_item=config_item, sub_items=['hierarchy', 'relationships'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'users':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'variants':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'wizards':
        sorted_items = get_items(config_item=config_item, sub_items=['configuration'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'workflowDefinitions':
        sorted_items = get_items(config_item=config_item, sub_items=['structure'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'workflows':
        sorted_items = get_items(config_item=config_item, sub_items=['variables', 'jobs'], filters=filters)
        save_items(config_item=config_item, items=sorted_items)
    elif config_item == 'workspaces':
        sorted_items = get_items(config_item=config_item, sub_items=[], filters=filters)
        save_items(config_item=config_item, items=sorted_items)

    return True


def pull_all() -> bool:
    """
    Pull all.

    :return: True if succeeds, False if fails
    """

    # accounts
    sorted_items = get_items(config_item="accounts", sub_items=['configuration', 'properties'])
    save_items(config_item='accounts', items=sorted_items)
    print('---')
    # actions
    sorted_items = get_items(config_item='actions', sub_items=['configuration'])
    save_items(config_item='actions', items=sorted_items)
    print('---')
    # collections
    sorted_items = get_items(config_item='collections', sub_items=['metadata'])
    save_items(config_item='collections', items=sorted_items)
    print('---')
    # event Handlers
    sorted_items = get_items(config_item='eventHandlers', sub_items=['configuration'])
    save_items(config_item='eventHandlers', items=sorted_items)
    print('---')
    # groups
    sorted_items = get_items(config_item='groups', sub_items=['members'])
    save_items(config_item='groups', items=sorted_items)
    print('---')
    # message Templates
    sorted_items = get_items(config_item='messageTemplates', sub_items=['body'])
    save_items(config_item='messageTemplates', items=sorted_items)
    print('---')
    # metadata Definitions
    sorted_items = get_items(config_item='metadataDefinitions', sub_items=['definition'])
    save_items(config_item='metadataDefinitions', items=sorted_items)
    print('---')
    # object Types
    sorted_items = get_items(config_item='objectTypes', sub_items=[])
    save_items(config_item='objectTypes', items=sorted_items)
    print('---')
    # profiles
    sorted_items = get_items(config_item='profiles', sub_items=['configuration'])
    save_items(config_item='profiles', items=sorted_items)
    print('---')
    # quotas
    sorted_items = get_items(config_item='quotas', sub_items=[])
    save_items(config_item='quotas', items=sorted_items)
    print('---')
    # resources
    sorted_items = get_items(config_item='resources', sub_items=['configuration'])
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
    # no way to retrieve taxonomies from API directly, so bypassing by reading tags from MD DEFs
    # NOTE: Will only retrieve taxonomies that are used by MD DEFs
    print("\nRetrieving taxonomies from Metadata Definitions as "
          "it is not possible to list them directly from the API...\nPlease note that only taxonomies that are used"
          " in metadata definitions will be retrieved.")
    metadata_definitions = get_items(config_item="metadataDefinitions", sub_items=['definition'])
    sorted_items = get_tags_and_taxonomies(metadata_definitions=metadata_definitions, mode=['taxonomies'])
    save_items(config_item='taxonomies', items=sorted_items)
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
    sorted_items = get_items(config_item='wizards', sub_items=['configuration'])
    save_items(config_item='wizards', items=sorted_items)
    print('---')
    # workflow Definitions
    sorted_items = get_items(config_item='workflowDefinitions', sub_items=['structure'])
    save_items(config_item='workflowDefinitions', items=sorted_items)
    print('---')
    # workspaces
    sorted_items = get_items(config_item='workspaces', sub_items=[])
    save_items(config_item='workspaces', items=sorted_items)

    return True


def create_script(item_name, item_config):
    """
    Create groovy script with according imports and plugins.

    :param item_name: script name
    :param item_config: script config
    :return:
    """

    imports = ["import com.ooyala.flex.plugins.PluginCommand\n"]
    script = "class Script extends PluginCommand {\n\t<&code>\n}"

    # jef
    try:
        imports.extend(['import ' + imp['value'] + '\n' for imp in
                        item_config['configuration']['instance']['internal-script']['script-import']])
    except:
        pass

    try:
        imports.extend(['import ' + imp['value'] + '\n' for imp in
                        item_config['configuration']['instance']['imports']['import']])
    except:
        pass

    # groovy decision
    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['script_type']['script'][:-2].replace("\n", "\n    ") + "\n\t}")
    except:
        pass

    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['internal-script']['script-content'][
                                :-2].replace("\n", "\n    ") + "\n\t}")
    except:
        pass

    # groovy script
    try:
        script = script.replace("<&code>",
                                item_config['configuration']['instance']['script-contents']['script'][:-2].replace("\n", "\n    ") + "\n\t}")
    except:
        script = script.replace("<&code>", "")

    content = f"{''.join(imports)}\n{script}"

    with open(f"{item_name}/script.groovy", "w") as groovy_file:
        groovy_file.write(content)
