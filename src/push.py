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

from tqdm import tqdm

from src.connect import get_default_account_id
from src.pull import save_items
from src.utils import get_items, reformat_tabs, reformat_spaces, get_auth_material, query

ACTION_UPDATE_FIELDS = [
    'accountId',
    'allowedAutoRetryAttempts',
    'autoRetryInterval',
    'concurrentJobsLimit',
    'description',
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


def push_command_func(args):
    """Action on push command. """

    # iterate over items to push
    # todo: temp fix
    item = " ".join(args.item_names)

        # if path exists
        if os.path.isdir(f"{args.config_item}/{item}"):

            # get obj
            with open(f"{args.config_item}/{item}/_object.json", 'r') as config_file:
                data = json.load(config_file)

            # action
            if args.config_item == 'actions' and data['objectType']['name'] == 'action':
                push_item(config_item=args.config_item, item_name=item, item_config=data,
                          push_and_retry_failed_jobs=args.push_to_failed_jobs)
            # job
            elif args.config_item == 'jobs' and data['objectType']['name'] == 'job':
                push_job(job_config=data)

            # event handlers
            elif args.config_item == 'eventHandlers' and data['objectType']['name'] == 'event-handler':
                push_item(config_item=args.config_item, item_name=item, item_config=data)

            # todo:
            #     eventHandlers
            #     groups
            #     messageTemplates
            #     metadataDefinitions
            #     profiles
            #     resources
            #     roles
            #     tagCollections
            #     taskDefinitions
            #     taxonomies
            #     timedActions
            #     userDefinedObjectTypes
            #     variants
            #     wizards
            #     workflowDefinitions
            #     workspaces

        else:
            print(f'Cannot push action {item} since it is not an action.\n')

    # for item in args.item_names:
    #
    #
    #
    #     # path doesn't exist
    #     else:
    #         print(f"Cannot find folder for {item}.\n")


def push_item(config_item: str, item_name: str, item_config: dict, restore: bool = False, push_and_retry_failed_jobs=False):
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
    item = query(method="GET", url=f"{config_item};name={item_name};exactNameMatch=true", log=False)
    total_count = item['totalCount']

    # item doesn't exist, create it
    if total_count == 0:

        # set action parameters
        payload['pluginClass'] = item_config['pluginClass']
        plugin = item_config['pluginClass']

        # plugin uuid if JEF
        if plugin in ["tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand",
                      "tv.nativ.mio.plugins.eventhandlers.jef.JefEventHandlerProxy"]:
            payload['pluginUuid'] = item_config['pluginUuid']

        # type only if action
        if config_item == 'actions':
            payload['type'] = item_config['type']['name']

        payload['visibilityIds'] = [get_default_account_id()]
        payload['accountId'] = get_default_account_id()

        # create item
        create_item = query(method="POST", url=f"{config_item}", payload=payload)
        item_id = create_item['id']

        # enable item
        if config_item in ['actions']:
            query(method="POST", url=f"{config_item}/{item_id}/actions", payload={"action": "enable"}, log=False)

    # item exists, update it
    elif total_count == 1:

        item_id = item.get(config_item)[0].get('id')
        plugin = item.get(config_item)[0].get('pluginClass')

        # create backup
        if not restore:
            backup = get_items(config_item=config_item, sub_items=['configuration'], filters=[f"id={item_id}"])
            save_items(config_item=config_item, items=backup, backup=True)

        # update item
        query(method="PUT", url=f"{config_item}/{item_id}", payload=payload)

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

            # reformat \r, \t and \s in code
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
            query(method="PUT", url=f"{config_item}/{item_id}/configuration", payload=payload)

            print(f"{config_item}: {item_name} has been pushed successfully to {env['url']}.\n") if not restore else \
                print(f"{config_item}: {item_name} has been restored successfully in {env['url']}.\n")

    # push config
    if os.path.isfile(f"{config_item}/{item_name}/configuration.json"):
        with open(f"{config_item}/{item_name}/configuration.json", 'r') as config_json:

            # build payload
            payload = json.load(config_json)

            # update configuration
            query(method="PUT", url=f"{config_item}/{item_id}/configuration", payload=payload)

            print(f"{config_item}: {item_name} has been pushed successfully to {env['url']}.\n") if not restore else \
                print(f"{config_item}: {item_name} has been restored successfully in {env['url']}.\n")
    print("---")

    # get updated action
    updated_action = get_items(config_item='actions', filters=[f"id={item_id}"])
    save_items(config_item='actions', items=updated_action)
    print("---")

    # push to failed jobs if needed
    if push_and_retry_failed_jobs:

        # retrieve failed jobs for given item
        failed_jobs = get_items(config_item="jobs",
                                filters=[f"name={item_name}", "exactNameMatch=true", "status=Failed"])

        for failed_job in tqdm(failed_jobs, desc="Pushing to failed jobs and retrying them"):
            # push script
            query(method="PUT", url=f"jobs/{failed_jobs.get(failed_job).get('id')}/configuration", payload=payload)

            # retry job
            query(method="POST", url=f"jobs/{failed_jobs.get(failed_job).get('id')}/actions",
                  payload={"action": "retry"})


def push_job(job_config: dict):
    """
        Push action for Flex.

        :param job_config: job config
        :return:
        """

    payload = {}
    job_id = job_config['id']
    imports = []

    # get auth material
    env, auth = get_auth_material()

    # check job exists
    job = query(method="GET", url=f"jobs/{job_id}")
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

            # reformat \r, \t and \s in code
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

            # update script
            query(method="PUT", url=f"jobs/{job_id}/configuration", payload=payload)

    # push config
    if os.path.isfile(f"jobs/{job_id}/configuration.json"):
        with open(f"jobs/{job_id}/configuration.json", 'r') as config_json:
            payload = json.load(config_json)

            # update configuration
            query(method="PUT", url=f"jobs/{job_id}/configuration", payload=payload)

    # retry job
    query(method="POST", url=f"jobs/{job_id}/actions", payload={"action": "retry"}, log=False)

    print(f"jobs: {job['name']} [{job_id}] has been pushed successfully to {env['url']} and has been retried.\n")

    print("---")

    # get updated item
    updated_job = get_items(config_item='jobs', filters=[f"id={job_id}"])
    save_items(config_item='jobs', items=updated_job)
