"""

    PROJECT: flex_toolbox
    FILENAME: create_action.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: create_action command
    
"""
import json

from VARIABLES import ACTION_CONFIG, DEFAULT_GROOVY_SCRIPT, WORKFLOW_CONFIG
from src.connect import get_default_account_id
from src.utils import create_folder


def create_action_command_func(args):
    """Action on create_action command. """

    quit() if not create_folder(folder_name=args.name) else None
    quit() if not create_object(name=args.name, type="action") else None


def create_object(name: str, type: str):
    """
    Create config

    :param name: object name
    :param type: type from [action, workflow]
    :return: True if created, False if failed
    """

    with open(name + "/config.json", "w") as config_file:
        if type == "action":
            # Creates config.json file
            config = ACTION_CONFIG
            config['name'] = name
            config['pluginClass'] = "tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand"
            config['accountId'] = get_default_account_id()
            config['visibilityIds'] = [get_default_account_id()]
            config['pluginUuid'] = "cab6f437-3ce0-4857-9578-fd519b783d66"
            json.dump(ACTION_CONFIG, config_file, indent=4)
            # Creates script.groovy file
            with open(name + "/script.groovy", "w") as groovy_file:
                groovy_file.write(DEFAULT_GROOVY_SCRIPT)
        elif type == "workflow":
            json.dump(WORKFLOW_CONFIG, config_file, indent=4)
        else:
            print(f"Cannot recognize object type. Aborting...")
            return False

    print(f"{name}/config.json with {type} config has been created.")
    return True
