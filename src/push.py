"""

    PROJECT: flex_toolbox
    FILENAME: push.py
    AUTHOR: David NAISSE
    DATE: September 14, 2023

    DESCRIPTION: push command functions
    
"""
import json
import os
import re

import requests
from requests.auth import HTTPBasicAuth

from src.connect import get_default_account_id
from src.env import get_default_env
from src.pull.pull import save_items
from src.utils import get_items, reformat_tabs, reformat_spaces

# global variables
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

# init. session
session = requests.Session()


def push_command_func(args):
    """Action on push command. """

    # iterate over items to push
    for item in args.item_names:

        # if path exists
        if os.path.isdir(f"{args.config_item}/{item}"):

            # check if is action
            with open(f"{args.config_item}/{item}/_object.json", 'r') as config_file:
                data = json.load(config_file)

            if args.config_item == 'actions' and data['objectType']['name'] == 'action':
                push_item(config_item=args.config_item, item_name=item, item_config=data)
            elif args.config_item == 'jobs' and data['objectType']['name'] == 'job':
                push_job(job_config=data)
            else:
                print(f'Cannot push action {item} since it is not an action.\n')

        # path doesn't exist
        else:
            print(f"Cannot find folder for {item}.\n")


def push_item(config_item: str, item_name: str, item_config: dict):
    """
    Push action for Flex.

    :param config_item: config entity
    :param item_name: item name
    :param item_config: item config
    :param restore: whether it's coming from a restore command or not
    :param push_and_retry_failed_jobs: whether to retry failed jobs or not
    :return:
    """

    # vars
    payload = {}
    item_id = item_config['id']
    imports = []
    plugin = None

    # retrieve auth material
    env, auth = get_auth_material()

    # build payload from item config
    for field in ACTION_UPDATE_FIELDS:
        if field in item_config:
            payload[field] = item_config.get(field)

    # check if action already exists first
    get_item = f"{env['url']}/api/{config_item};name={item_name};exactNameMatch=true"
    item = session.request("GET", get_item, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    if 'errors' in item:
        raise Exception(f"\n\nError while sending {get_item}. \nError message: {item['errors']['error']}\n ")

    total_count = item['totalCount']

    # action doesn't exist, create it
    if total_count == 0:

        # set action parameters
        payload['pluginClass'] = item_config['pluginClass']
        plugin = item_config['pluginClass']

        if plugin == "tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand":
            payload['pluginUuid'] = item_config['pluginUuid']

        payload['type'] = item_config['type']['name']
        payload['visibilityIds'] = [get_default_account_id()]
        payload['accountId'] = get_default_account_id()

        # create action
        create_item_request = f"{env['url']}/api/{config_item}"
        print(f"\nPerforming [POST] {env['url']}/api/{config_item}...")
        create_item = session.request("POST", create_item_request, headers=HEADERS, auth=auth,
                                      data=json.dumps(payload)).json()

        if 'errors' in create_item:
            raise Exception(
                f"\n\nError while sending {create_item_request}. \nError message: {create_item['errors']['error']}\n")

        item_id = create_item['id']

        # enable action
        enable_item_request = f"{env['url']}/api/{config_item}/{item_id}/actions"
        enable_item = session.request("POST", enable_item_request, headers=HEADERS, auth=auth,
                                      data=json.dumps({"action": "enable"})).json()

        if 'errors' in enable_item:
            raise Exception(
                f"\n\nError while sending {enable_item_request}. \nError message: {enable_item['errors']['error']}\n")

    # action exists, update it
    elif total_count == 1:

        item_id = item.get(config_item)[0].get('id')
        plugin = item.get(config_item)[0].get('pluginClass')

        # create backup
        if not restore:
            backup = get_items(config_item='actions', sub_items=['configuration'], filters=[f"id={item_id}"])
            save_items(config_item='actions', items=backup, backup=True)

        # update action
        update_action_request = f"{env['url']}/api/{config_item}/{item_id}"
        print(f"\nPerforming [PUT] {update_action_request}...")
        update_action = session.request("PUT", update_action_request, headers=HEADERS, auth=auth,
                                        data=json.dumps(payload)).json()

        if 'errors' in update_action:
            raise Exception(
                f"\n\nError while sending {update_action_request}. \nError message: {update_action['errors']['error']}\n")

    # push script
    if os.path.isfile(f"{config_item}/{item_name}/script.groovy"):
        with open(f"{config_item}/{item_name}/script.groovy", 'r') as groovy_file:
            script_content = groovy_file.read().strip() \
                .replace("import com.ooyala.flex.plugins.PluginCommand", "")

            # get imports
            for line in script_content.split("\n"):
                if line.startswith("import") and "PluginCommand" not in line:
                    imports.append({'value': line[7:], 'isExpression': False})
                    script_content = script_content.replace(line + "\n", "")

            # get code
            last_char = script_content.rindex("}")
            script_content = script_content[:last_char - 2].replace("class Script extends PluginCommand {",
                                                                    "").strip() + "\n}"

            script_content = re.sub(r'\t{1,}', reformat_tabs, script_content)
            script_content = re.sub(r' {4,}', reformat_spaces, script_content)

            try:
                exec_lock_type = item_config['configuration']['instance']['execution-lock-type']
            except:
                exec_lock_type = "NONE"

            # jef
            if plugin == "tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand":

                # script
                payload = {
                    "internal-script": {
                        "script-content": script_content,
                    },
                    "execution-lock-type": exec_lock_type
                }

                # imports
                if imports:
                    payload['internal-script']['script-import'] = imports
            # groovy script
            elif plugin == "tv.nativ.mio.plugins.actions.script.GroovyScriptCommand":

                # payload
                payload = {
                    "script-contents": {
                        "script": script_content,
                    },
                }

                # imports
                if imports:
                    payload['imports'] = {"import": imports}

            # groovy decision
            elif plugin == "tv.nativ.mio.plugins.actions.decision.ScriptedDecisionCommand" or \
                    "tv.nativ.mio.plugins.actions.decision.multi.ScriptedMultiDecisionCommand":

                # payload
                payload = {
                    "script_type": {
                        "script": script_content,
                    },
                }

                # imports
                if imports:
                    payload['imports'] = {"import": imports}

            # update configuration
            update_configuration_request = f"{env['url']}/api/{config_item}/{item_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()

            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

            print(f"{config_item}: {item_name} has been pushed successfully to {env['url']}.\n") if not restore else \
                print(f"{config_item}: {item_name} has been restored successfully in {env['url']}.\n")

    # push config
    if os.path.isfile(f"{config_item}/{item_name}/configuration.json"):
        with open(f"{config_item}/{item_name}/configuration.json", 'r') as config_json:

            # build payload
            payload = json.load(config_json)

            # update configuration
            update_configuration_request = f"{env['url']}/api/{config_item}/{item_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()
            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

            print(f"{config_item}: {item_name} has been pushed successfully to {env['url']}.\n") if not restore else \
                print(f"{config_item}: {item_name} has been restored successfully in {env['url']}.\n")
    print("---")

    # get updated action
    updated_action = get_items(config_item='actions', filters=[f"id={item_id}"])
    save_items(config_item='actions', items=updated_action)
    print("---")

    # push to failed jobs if needed
    if push_and_retry_failed_jobs:
        failed_jobs = get_items(config_item="jobs", filters=[f"name={item_name}", "exactNameMatch=true", "status=Failed"])

        for failed_job in tqdm(failed_jobs, desc="Pushing to failed jobs and retrying them"):
            push_script_request = f"{env['url']}/api/jobs/{failed_jobs.get(failed_job).get('id')}/configuration"
            push_script = session.request("PUT", push_script_request, headers=HEADERS, auth=auth,
                                          data=json.dumps(payload)).json()

            # retry job
            retry_job_request = f"{env['url']}/api/jobs/{failed_jobs.get(failed_job).get('id')}/actions"
            session.request("POST", retry_job_request, headers=HEADERS, auth=auth,
                            data=json.dumps({"action": "retry"})).json()


def push_job(job_config: dict):
    """
        Push action for Flex.

        :param job_config: job config
        :return:
        """

    payload = {}
    job_id = job_config['id']
    imports = []

    # Retrieve default env
    env = get_default_env()

    # Init. connection & auth with env API
    auth = HTTPBasicAuth(username=env['username'], password=env['password'])

    # check job exists
    job_request = f"{env['url']}/api/jobs/{job_id}"
    job = session.request("GET", job_request, headers=HEADERS, auth=auth, data=PAYLOAD).json()

    # exception handler
    if 'errors' in job:
        raise Exception(f"\n\nError while sending {job_request}. \nError message: {job['errors']['error']}\n ")
    else:
        job_id = job['id']
        plugin = job['action']['pluginClass']

    # push script
    if os.path.isfile(f"jobs/{job_id}/script.groovy"):
        with open(f"jobs/{job_id}/script.groovy", 'r') as groovy_file:
            script_content = groovy_file.read().strip() \
                .replace("import com.ooyala.flex.plugins.PluginCommand", "")

            # get imports
            for line in script_content.split("\n"):
                if line.startswith("import") and "PluginCommand" not in line:
                    imports.append({'value': line[7:], 'isExpression': False})
                    script_content = script_content.replace(line, "")

            # get code
            last_char = script_content.rindex("}")
            script_content = script_content[:last_char - 2].replace("class Script extends PluginCommand {",
                                                                    "").strip() + "\n}"

            script_content = re.sub(r'\t{1,}', reformat_tabs, script_content)
            script_content = re.sub(r' {4,}', reformat_spaces, script_content)

            try:
                exec_lock_type = job_config['configuration']['instance']['execution-lock-type']
            except:
                exec_lock_type = "NONE"

            # jef
            if plugin == "tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand":

                # script
                payload = {
                    "internal-script": {
                        "script-content": script_content,
                    },
                    "execution-lock-type": exec_lock_type
                }

                # imports
                if imports:
                    payload['internal-script']['script-import'] = imports
            # groovy script
            elif plugin == "tv.nativ.mio.plugins.actions.script.GroovyScriptCommand":

                # payload
                payload = {
                    "script-contents": {
                        "script": script_content,
                    },
                }

                # imports
                if imports:
                    payload['imports'] = {"import": imports}

            # groovy decision
            elif plugin == "tv.nativ.mio.plugins.actions.decision.ScriptedDecisionCommand" or \
                    "tv.nativ.mio.plugins.actions.decision.multi.ScriptedMultiDecisionCommand":

                # payload
                payload = {
                    "script_type": {
                        "script": script_content,
                    },
                }

                # imports
                if imports:
                    payload['imports'] = {"import": imports}

            # update configuration
            update_configuration_request = f"{env['url']}/api/jobs/{job_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()

            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

    # push config
    if os.path.isfile(f"jobs/{job_id}/configuration.json"):
        with open(f"jobs/{job_id}/configuration.json", 'r') as config_json:
            payload = json.load(config_json)

            # update configuration
            update_configuration_request = f"{env['url']}/api/jobs/{job_id}/configuration"
            print(f"\nPerforming [PUT] {update_configuration_request}...\n")
            update_configuration = session.request("PUT", update_configuration_request, headers=HEADERS, auth=auth,
                                                   data=json.dumps(payload)).json()
            # exception handler
            if 'errors' in update_configuration:
                raise Exception(
                    f"\n\nError while sending {update_configuration_request}. \nError message: {update_configuration['errors']['error']}\n")

    # retry job
    retry_job_request = f"{env['url']}/api/jobs/{job_id}/actions"
    session.request("POST", retry_job_request, headers=HEADERS, auth=auth,
                    data=json.dumps({"action": "retry"})).json()

    print(f"jobs: {job['name']} [{job_id}] has been pushed successfully to {env['url']} and has been retried.\n")

    print("---")

    # get updated item
    updated_job = get_items(config_item='jobs', filters=[f"id={job_id}"])
    save_items(config_item='jobs', items=updated_job)
