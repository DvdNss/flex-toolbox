"""

    PROJECT: flex_toolbox
    FILENAME: push.py
    AUTHOR: David NAISSE
    DATE: September 14, 2023

    DESCRIPTION: TODO
    
"""
import json
import os

import requests
from requests.auth import HTTPBasicAuth

from src.connect import get_default_account_id
from src.env import get_default_env

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
        if os.path.isdir(item):

            # check if is action
            with open(f"{item}/config.json", 'r') as config_file:
                data = json.load(config_file)

            if data['objectType']['name'] == 'action':
                push_action(action_name=item, action_config=data)

        # path doesn't exist
        else:
            print(f"Cannot find folder for {item}.")


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
    total_count = session.request("GET", get_action, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    if 'errors' in total_count:
        raise Exception(f"\n\nError while sending {get_action}. \nError message: {total_count['errors']['error']} ")

    total_count = total_count['totalCount']

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
        create_action = session.request("POST", create_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps(payload)).json()

        if 'errors' in create_action:
            raise Exception(
                f"\n\nError while sending {create_action_request}. \nError message: {create_action['errors']['error']} ")

        # push script
        action_id = create_action['id']

    # action exists, update it
    elif total_count == 1:

        # update action
        update_action_request = f"{env['url']}/api/actions/{action_id}"
        update_action = session.request("PUT", update_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps(payload)).json()

        if 'errors' in update_action:
            raise Exception(
                f"\n\nError while sending {update_action_request}. \nError message: {update_action['errors']['error']} ")

    # push script
    if os.path.isfile(f"{action_name}/script.groovy"):
        with open(f"{action_name}/script.groovy", 'r') as groovy_file:
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

            payload = {
                "internal-script": {
                    "script-content": script_content,
                    "script-import": imports if imports else None
                },
                "execution-lock-type": action_config['configuration']['instance']['execution-lock-type']
            }

            # update configuration
            update_configuration_request = f"{env['url']}/api/actions/{action_id}/configuration"
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()

            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']} ")
