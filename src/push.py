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
from src.env import get_default_env_alias
from src.pull import save_items
from src.utils import get_items, reformat_tabs, reformat_spaces, query, enumerate_sub_items

UPDATE_FIELDS = [
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

    # get default env alias if not specified in args
    src_environment = get_default_env_alias() if args.from_ == 'default' else args.from_
    dest_environments = [get_default_env_alias()] if args.to == ['default'] else args.to

    # build item name
    item = " ".join(args.item_names)

    # todo: temp fix join bcz jenkins container split args by space

    # if path exists
    if os.path.isdir(f"{src_environment}/{args.config_item}/{item}"):

        # get obj
        with open(f"{src_environment}/{args.config_item}/{item}/_object.json", 'r') as config_file:
            data = json.load(config_file)

        # iterate over dest envs
        for dest_environment in dest_environments:
            push_item(
                config_item=args.config_item,
                item_name=item,
                item_config=data,
                push_and_retry_failed_jobs=args.push_to_failed_jobs,
                src_environment=src_environment,
                dest_environment=dest_environment
            )
    else:
        print(f"Cannot find {src_environment}/{args.config_item}/{item}. Please check the information provided. ")


def push_item(config_item: str, item_name: str, item_config: dict, restore: bool = False,
              push_and_retry_failed_jobs=False, src_environment: str = "default", dest_environment: str = "default"):
    """
    Push action for Flex.

    :param config_item: config entity
    :param item_name: item name
    :param item_config: item config
    :param restore: whether it's coming from a restore command or not
    :param push_and_retry_failed_jobs: whether to retry failed jobs or not
    :param src_environment: src environment
    :param dest_environment: dest environment
    :return:
    """

    # vars
    payload = {}
    item_id = item_config['id']
    imports = []
    plugin = None
    is_item_instance = False

    # build payload from item config
    for field in UPDATE_FIELDS:
        if field in item_config:
            payload[field] = item_config.get(field)

    # id-based or name-based query
    if config_item in ['jobs', 'workflows']:
        query_content = f"id={item_id}"
        is_item_instance = True
    else:
        query_content = f"name={item_name};exactNameMatch=true"

    # check if item already exists first
    item = query(method="GET", url=f"{config_item};{query_content}", log=False,
                 environment=dest_environment)
    total_count = item['totalCount']

    # item doesn't exist, create it
    if total_count == 0 and not is_item_instance:
        # todo: taxonomies create
        # todo: workflow create

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

        payload['visibilityIds'] = [get_default_account_id(environment=dest_environment)]
        payload['accountId'] = get_default_account_id(environment=dest_environment)

        # create item
        create_item = query(method="POST", url=f"{config_item}", payload=payload, environment=dest_environment)
        item_id = create_item['id']

        # enable item
        if config_item in ['actions']:
            query(method="POST", url=f"{config_item}/{item_id}/actions", payload={"action": "enable"}, log=False,
                  environment=dest_environment)

    # item exists, update it
    elif total_count == 1 and not is_item_instance:

        item_id = item.get(config_item)[0].get('id')
        plugin = item.get(config_item)[0].get('pluginClass')

        # create backup
        if not restore:
            backup = get_items(config_item=config_item, sub_items=['configuration'], filters=[f"id={item_id}"],
                               environment=dest_environment)
            save_items(config_item=config_item, items=backup, backup=True, environment=dest_environment)

        # update item
        query(method="PUT", url=f"{config_item}/{item_id}", payload=payload, environment=dest_environment)

    # push script
    if os.path.isfile(f"{src_environment}/{config_item}/{item_name}/script.groovy"):
        with open(f"{src_environment}/{config_item}/{item_name}/script.groovy", 'r') as groovy_file:
            script_content = groovy_file.read().strip() \
                .replace("import com.ooyala.flex.plugins.PluginCommand", "")

            # get imports
            for line in script_content.split("\n"):
                if line.startswith("import") and "PluginCommand" not in line:
                    imports.append({'value': line[7:], 'isExpression': False})
                    script_content = script_content.replace(line + "\n", "")

            # get code
            last_char = script_content.rindex("}")
            script_content = script_content[:last_char - 1].replace("class Script extends PluginCommand {", "")

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
                if config_item != 'timedActions':
                    payload = {
                        "internal-script": {
                            "script-content": script_content,
                        },
                        "execution-lock-type": exec_lock_type
                    }
                else:
                    payload = {
                        "internal-script": {
                            "script-content": script_content,
                        },
                        "polling-time-period": item_config['configuration']['instance']['polling-time-period'],
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
            query(method="PUT", url=f"{config_item}/{item_id}/configuration", payload=payload,
                  environment=dest_environment)

            print(
                f"{src_environment}/{config_item}: {item_name} has been pushed successfully to {dest_environment}.\n") if not restore else \
                print(
                    f"{src_environment}/{config_item}: {item_name} has been restored successfully in {dest_environment}.\n")

    # push config
    for item_property in ['configuration', 'metadata', 'definition']:
        if os.path.isfile(f"{src_environment}/{config_item}/{item_name}/{item_property}.json"):
            with open(f"{src_environment}/{config_item}/{item_name}/{item_property}.json", 'r') as config_json:
                # build payload
                payload = json.load(config_json)

                # update configuration
                query(method="PUT", url=f"{config_item}/{item_id}/{item_property}", payload=payload,
                      environment=dest_environment)

                print(
                    f"{src_environment}/{config_item} [{item_property}]: {item_name} has been pushed successfully to {dest_environment}.\n") if not restore else \
                    print(
                        f"{src_environment}/{config_item} [{item_property}]: {item_name} has been restored successfully in {dest_environment}.\n")
    print("---")

    # retry
    if is_item_instance:
        query(method="POST", url=f"{config_item}/{item_id}/actions", payload={"action": "retry"}, log=False)

    # get updated action
    updated_item = get_items(config_item=config_item, sub_items=enumerate_sub_items(config_item=config_item),
                             filters=[f"id={item_id}"], environment=dest_environment)
    save_items(config_item=config_item, items=updated_item, environment=dest_environment)
    print("---")

    # push to failed jobs if needed
    if push_and_retry_failed_jobs:

        # retrieve failed jobs for given item
        failed_jobs = get_items(config_item="jobs",
                                filters=[f"name={item_name}", "exactNameMatch=true", "status=Failed"],
                                environment=dest_environment)

        for failed_job in tqdm(failed_jobs, desc="Pushing to failed jobs and retrying them"):
            # push script
            query(method="PUT", url=f"jobs/{failed_jobs.get(failed_job).get('id')}/configuration", payload=payload,
                  environment=dest_environment)

            # retry job
            query(method="POST", url=f"jobs/{failed_jobs.get(failed_job).get('id')}/actions",
                  payload={"action": "retry"}, environment=dest_environment)
