"""

    PROJECT: flex_toolbox
    FILENAME: push.py
    AUTHOR: David NAISSE
    DATE: September 14, 2023

    DESCRIPTION: push command functions
    
"""
import json
import os

import requests
from requests.auth import HTTPBasicAuth

from src.connect import get_default_account_id
from src.env import get_default_env
from src.pull import save_items
from src.utils import get_items

# Global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}
ACTION_UPDATE_FIELDS = [
    'accountId',
    'allowedAutoRetryAttempts',
    'autoRetryInterval',
    'concurrentJobsLimit',
    'description',
    'externalIds',
    'name',
    'priority',
    'redoAction',
    'runRuleExpression',
    'supportsAutoRetry',
    'timeout',
    'undoAction',
    'useLatestAvailableVersion',
    'visibilityIds'
]

# Init. session
session = requests.Session()


def push_command_func(args):
    """Action on pull command. """

    # iterate over items to push
    for item in args.item_names:

        # if path exists
        if os.path.isdir(f"{args.config_item}/{item}"):

            # check if is action
            with open(f"{args.config_item}/{item}/_object.json", 'r') as config_file:
                data = json.load(config_file)

            if args.config_item == 'actions' and data['objectType']['name'] == 'action':
                push_action(action_name=item, action_config=data)
            else:
                print(f'Cannot push action {item} since it is not an action.\n')

        # path doesn't exist
        else:
            print(f"Cannot find folder for {item}.\n")


def push_action(action_name, action_config):
    """
    Push action for Flex.

    :param action_name: action to push
    :param action_config: action config
    :return:
    """

    payload = {}
    action_id = action_config['id']
    imports = []

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # build payload
    for field in ACTION_UPDATE_FIELDS:
        if field in action_config:
            payload[field] = action_config[field]

    # check if action already exists first
    get_action = f"{env['url']}/api/actions;name={action_name}"
    response = session.request("GET", get_action, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    if 'errors' in response:
        raise Exception(f"\n\nError while sending {get_action}. \nError message: {response['errors']['error']}\n ")

    total_count = response['totalCount']

    # action doesn't exist, create it
    if total_count == 0:

        # set action parameters
        payload['pluginClass'] = action_config['pluginClass']
        payload['pluginUuid'] = action_config['pluginUuid']
        payload['type'] = action_config['type']['name']
        payload['visibilityIds'] = [get_default_account_id()]
        payload['accountId'] = get_default_account_id()

        # create action
        create_action_request = f"{env['url']}/api/actions"
        print(f"\nPerforming [POST] {env['url']}/api/actions...")
        create_action = session.request("POST", create_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps(payload)).json()

        if 'errors' in create_action:
            raise Exception(
                f"\n\nError while sending {create_action_request}. \nError message: {create_action['errors']['error']}\n")

        action_id = create_action['id']

        # enable action
        enable_action_request = f"{env['url']}/api/actions/{action_id}/actions"
        enable_action = session.request("POST", enable_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps({"action": "enable"})).json()

        if 'errors' in enable_action:
            raise Exception(
                f"\n\nError while sending {enable_action_request}. \nError message: {enable_action['errors']['error']}\n")

    # action exists, update it
    elif total_count == 1:

        action = get_items(config_item='actions', filters=[f"name={action_name}"])
        action_id = action.get(next(iter(action))).get('id')

        # update action
        update_action_request = f"{env['url']}/api/actions/{action_id}"
        print(f"\nPerforming [PUT] {update_action_request}...")
        update_action = session.request("PUT", update_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps(payload)).json()

        if 'errors' in update_action:
            raise Exception(
                f"\n\nError while sending {update_action_request}. \nError message: {update_action['errors']['error']}\n")

    # push script
    if os.path.isfile(f"actions/{action_name}/script.groovy"):
        with open(f"actions/{action_name}/script.groovy", 'r') as groovy_file:
            script_content = groovy_file.read().strip() \
                .replace("import com.ooyala.flex.plugins.PluginCommand", "")

            # get imports
            for line in script_content.split("\n"):
                if line.startswith("import") and "PluginCommand" not in line:
                    imports.append({'value': line[7:], 'isExpression': False})
                    script_content = script_content.replace(line, "")

            # get code
            last_char = script_content.rindex("}")
            script_content = script_content[:last_char - 2].replace("class Script extends PluginCommand {\n\t",
                                                                    "").replace("\t\t", '\t').strip() + "\n}"
            try:
                exec_lock_type = action_config['configuration']['instance']['execution-lock-type']
            except:
                exec_lock_type = "NONE"

            payload = {
                "internal-script": {
                    "script-content": script_content,
                    "script-import": imports if imports else None
                },
                "execution-lock-type": exec_lock_type
            }

            # update configuration
            update_configuration_request = f"{env['url']}/api/actions/{action_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()

            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

            print(f"action: {action_name} has been pushed successfully to {env['url']}.\n")

    # push config
    if os.path.isfile(f"actions/{action_name}/configuration.json"):
        with open(f"actions/{action_name}/configuration.json", 'r') as config_json:
            payload = json.load(config_json)

            # update configuration
            update_configuration_request = f"{env['url']}/api/actions/{action_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()
            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

            print(f"action: {action_name} has been pushed successfully to {env['url']}.\n")

    print("---")

    # get updated action
    updated_action = get_items(config_item='actions', filters=[f"id={action_id}"])
    save_items(config_item='actions', items=updated_action)
