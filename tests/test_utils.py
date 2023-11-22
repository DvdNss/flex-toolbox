"""

    PROJECT: flex_toolbox
    FILENAME: test_utils.py
    AUTHOR: David NAISSE
    DATE: November 13, 2023

    DESCRIPTION: tests for utils.py
    
"""
import os
from unittest import TestCase

from src.utils import kebab_to_camel_case, create_script, query, get_auth_material, dig_for_tags_and_taxonomies, \
    get_taxonomies, find_nested_dependencies, get_nested_value, get_full_items, apply_post_retrieval_filters


class TestUtils(TestCase):
    """Tests for utils.py"""

    def test_kebab_to_camel_case(self):
        # ins
        input = "event-handler"

        # outs
        output = kebab_to_camel_case(input)

        # test
        assert output == "eventHandlers", f"Should be eventHandlers, is {input}."

    def test_create_script(self):
        # ins
        item_name = "pyUnitTest"
        item_config = {
            "configuration": {
                "instance": {
                    "internal-script": {
                        "script-content": "def execute() {\n\tcontext.logInfo('test')\n}",
                        "script-import": [
                            {
                                "value": "groovy.json.JsonSlurper"
                            }
                        ]
                    }
                }
            }
        }

        # outs
        os.mkdir(item_name)
        test_create = create_script(item_name=item_name, item_config=item_config)

        # reset
        os.remove(f"{item_name}/script.groovy")
        os.removedirs(f"{item_name}")

        # test
        expected = "import com.ooyala.flex.plugins.PluginCommand\nimport groovy.json.JsonSlurper\n\nclass Script extends PluginCommand {\n\tdef execute() {\n\t\tcontext.logInfo('test')\n\t}\n}"
        assert test_create == expected

    def test_query_valid(self):
        # ins
        method, url, environment = "GET", "resources;limit=1", "default"

        # outs
        response = query(method=method, url=url, log=False, environment=environment)

        # test
        assert 'resources' in response and len(response['resources']) != 0

    def test_query_invalid(self):
        # ins
        method, url, environment = "GET", "resources;invalid", "default"

        # outs
        try:
            query(method=method, url=url, log=False, environment=environment)

            # test
            self.fail()
        except Exception as ex:
            assert "Error message: " in str(ex) and "invalid" in str(ex)

    def test_get_auth_material_valid(self):
        # ins
        environment = "default"

        # outs
        try:
            get_auth_material(environment=environment)
        except:
            self.fail()

    def test_get_auth_material_invalid(self):
        # ins
        environments = "invalid"

        # outs
        try:
            get_auth_material(environment=environments)
            self.fail()
        except KeyError as ke:
            assert "invalid" in str(ke)

    def test_get_tags_and_taxonomies_tags(self):
        # ins
        tags = []
        entries = [
            # depth = 1
            {
                "backingStoreType": "USER_DEFINED_TAG_COLLECTION",
                "backingStoreInstanceId": 7465,
            },
            # depth > 1
            {
                "children":
                    [
                        {
                            "backingStoreType": "USER_DEFINED_TAG_COLLECTION",
                            "backingStoreInstanceId": 74650,
                        },
                    ]

            }
        ]

        # outs
        dig_for_tags_and_taxonomies(entries=entries, tags=tags, taxonomies=[])

        # test
        assert tags == [7465, 74650]

    def test_get_tags_and_taxonomies_taxonomies(self):
        # ins
        taxonomies = []
        entries = [
            # depth =1
            {
                "backingStoreType": "TAXONOMY",
                "filter": "000",
            },
            # depth > 1
            {
                "children":
                    [
                        {
                            "backingStoreType": "TAXONOMY",
                            "filter": "001",
                        },
                    ]

            }
        ]

        # outs
        dig_for_tags_and_taxonomies(entries=entries, tags=[], taxonomies=taxonomies)

        # test
        assert taxonomies == ["000", "001"]

    def test_get_taxonomies_valid(self):
        # ins
        filters = ["enabled=true"]

        # outs
        try:
            taxonomies = get_taxonomies(filters=filters, log=False)
            assert isinstance(taxonomies, list)
        except:
            self.fail()

    def test_find_nested_dependencies(self):
        # ins
        data = {
            "id": 999,
            "nested_1": {
                "id": 111,
                "nested_2": {
                    "id": 222,
                }
            }
        }

        # outs
        dependencies = find_nested_dependencies(data=data)

        # test
        assert dependencies == ['nested_1', 'nested_1.nested_2']

    def test_get_nested_value_valid(self):
        # ins
        key = "nested_key"
        data = {
            "nested_1": {
                "nested_2": {
                    "key": "value"
                }
            }
        }

        # outs
        nested_value = get_nested_value(obj=data, keys="nested_1.nested_2.key")

        # test
        assert nested_value == "value"

    def test_get_nested_value_invalid(self):
        # ins
        key = "nested_1.nested_2.key"
        data = {
            "nested_1":
                [{
                    "nested_2": {
                        "key": "value"
                    }
                }]
        }

        # outs
        nested_value = get_nested_value(obj=data, keys=key)

        # test
        assert not nested_value

    def test_get_full_items_accounts(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "accounts", ['limit=1'], [], False

        # outs
        accounts = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(accounts, dict) and (accounts.get(list(accounts.keys())[0]).get('objectType').get(
            'name') in ['account', 'master-account'] if len(list(accounts.keys())) != 0 else True)

    def test_get_full_items_actions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "actions", ['limit=1'], [], False

        # outs
        actions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(actions, dict) and (actions.get(list(actions.keys())[0]).get('objectType').get(
            'name') == 'action' if len(list(actions.keys())) != 0 else True)

    def test_get_full_items_assets(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "assets", ['limit=1'], [], False

        # outs
        assets = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(assets, dict) and (
            "id" in assets.get(list(assets.keys())[0]) if len(list(assets.keys())) != 0 else True)

    def test_get_full_items_collections(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "collections", ['limit=1'], [], False

        # outs
        collections = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(collections, dict) and (
            "uuid" in collections.get(list(collections.keys())[0]) if len(list(collections.keys())) != 0 else True)

    def test_get_full_items_event_handlers(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "eventHandlers", ['limit=1'], [], False

        # outs
        event_handlers = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(event_handlers, dict) and (event_handlers.get(list(event_handlers.keys())[0]).get(
            'objectType').get(
            'name') == 'event-handler' if len(list(event_handlers.keys())) != 0 else True)

    def test_get_full_items_events(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "events", ['limit=1'], [], False

        # outs
        events = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(events, dict) and (
            events.get(list(events.keys())[0]).get('id') if len(list(events.keys())) != 0 else True)

    def test_get_full_items_groups(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "groups", ['limit=1'], [], False

        # outs
        groups = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(groups, dict) and (
            groups.get(list(groups.keys())[0]).get('objectType').get('name') == 'group' if len(
                list(groups.keys())) != 0 else True)

    def test_get_full_items_jobs(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "jobs", ['limit=1'], [], False

        # outs
        jobs = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(jobs, dict) and (jobs.get(list(jobs.keys())[0]).get('objectType').get(
            'name') == 'job' if len(list(jobs.keys())) != 0 else True)

    def test_get_full_items_message_templates(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "messageTemplates", ['limit=1'], [], False

        # outs
        messsage_templates = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(messsage_templates, dict) and (messsage_templates.get(list(messsage_templates.keys())[0]).get(
            'objectType').get(
            'name') == 'message-template' if len(list(messsage_templates.keys())) != 0 else True)

    def test_get_full_items_metadata_definitions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "metadataDefinitions", ['limit=1'], [], False

        # outs
        metadata_definitions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(metadata_definitions, dict) and (metadata_definitions.get(
            list(metadata_definitions.keys())[0]).get('objectType').get('name') == 'metadata-definition' if len(
            list(metadata_definitions.keys())) != 0 else True)

    def test_get_full_items_object_types(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "objectTypes", ['limit=1'], [], False

        # outs
        object_types = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(object_types, dict) and (
            object_types.get(list(object_types.keys())[0]).get('id') if len(list(object_types.keys())) != 0 else True)

    def test_get_full_items_profiles(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "profiles", ['limit=1'], [], False

        # outs
        profiles = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(profiles, dict) and (profiles.get(list(profiles.keys())[0]).get('objectType').get('name') \
                                               == 'profile' if len(list(profiles.keys())) != 0 else True)

    def test_get_full_items_quotas(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "quotas", ['limit=1'], [], False

        # outs
        quotas = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(quotas, dict) and (quotas.get(list(quotas.keys())[0]).get('objectType').get('name') \
                                             == 'quota' if len(list(quotas.keys())) != 0 else True)

    def test_get_full_items_resources(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "resources", ['limit=1'], [], False

        # outs
        resources = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(resources, dict) and (resources.get(list(resources.keys())[0]).get('objectType').get('name') \
                                                == 'resource' if len(list(resources.keys())) != 0 else True)

    def test_get_full_items_roles(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "roles", ['limit=1'], [], False

        # outs
        roles = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(roles, dict) and (
            roles.get(list(roles.keys())[0]).get('objectType').get('name') \
            == 'role' if len(list(roles.keys())) != 0 else True)

    def test_get_full_items_task_definitions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "taskDefinitions", ['limit=1'], [], False

        # outs
        task_definitions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(task_definitions, dict) and (
            task_definitions.get(list(task_definitions.keys())[0]).get('objectType').get('name') \
            == 'task-definition' if len(list(task_definitions.keys())) != 0 else True)

    def test_get_full_items_tasks(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "tasks", ['limit=1'], [], False

        # outs
        tasks = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(tasks, dict) and (
            tasks.get(list(tasks.keys())[0]).get('objectType').get('name') \
            == 'task' if len(list(tasks.keys())) != 0 else True)

    def test_get_full_items_timed_actions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "timedActions", ['limit=1'], [], False

        # outs
        timed_actions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(timed_actions, dict) and (
            timed_actions.get(list(timed_actions.keys())[0]).get('objectType').get('name') \
            == 'timed-action' if len(list(timed_actions.keys())) != 0 else True)

    def test_get_full_items_user_defined_object_types(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "userDefinedObjectTypes", [], [], False

        # outs
        user_defined_object_types = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(user_defined_object_types, dict) and (
            user_defined_object_types.get(list(user_defined_object_types.keys())[0]).get('objectType').get('name') \
            == 'user-defined-object-type' if len(list(user_defined_object_types.keys())) != 0 else True)

    def test_get_full_items_users(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "users", ['limit=1'], [], False

        # outs
        users = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(users, dict) and (
            users.get(list(users.keys())[0]).get('objectType').get('name') \
            == 'user' if len(list(users.keys())) != 0 else True)

    def test_get_full_items_variants(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "variants", ['limit=1'], [], False

        # outs
        variants = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(variants, dict) and (
            variants.get(list(variants.keys())[0]).get('objectType').get('id') if len(
                list(variants.keys())) != 0 else True)

    def test_get_full_items_wizards(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "wizards", ['limit=1'], [], False

        # outs
        wizards = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(wizards, dict) and (
            wizards.get(list(wizards.keys())[0]).get('objectType').get('name') == 'wizard' if len(
                list(wizards.keys())) != 0 else True)

    def test_get_full_items_workflow_definitions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "workflowDefinitions", ['limit=1'], [], False

        # outs
        workflow_definitions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(workflow_definitions, dict) and (
            workflow_definitions.get(list(workflow_definitions.keys())[0]).get('objectType').get(
                'name') == 'workflow-definition' if len(
                list(workflow_definitions.keys())) != 0 else True)

    def test_get_full_items_workflows(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "workflows", ['limit=1'], [], False

        # outs
        workflows = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(workflows, dict) and (
            workflows.get(list(workflows.keys())[0]).get('objectType').get('name') == 'workflow' if len(
                list(workflows.keys())) != 0 else True)

    def test_get_full_items_workspaces(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "workspaces", ['limit=1'], [], False

        # outs
        workspaces = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False
        )

        # test
        assert isinstance(workspaces, dict) and (
            workspaces.get(list(workspaces.keys())[0]).get('objectType').get('name') == 'workspace' if len(
                list(workspaces.keys())) != 0 else True)

    def test_apply_post_retrieval_filters(self):
        # ins
        filters = ['not_nested_key>0', 'nested.nested_key!=0']
        items = {
            "item_1": {
                "not_nested_key": 0,
                "nested": {
                    "nested_key": 0
                }
            },
            "item_2": {
                "not_nested_key": 1,
                "nested": {
                    "nested_key": 1
                }
            }
        }

        # outs
        filtered_items = apply_post_retrieval_filters(items=items, filters=filters, log=False)

        # test
        assert filtered_items == {"item_2": {"not_nested_key": 1, "nested": {"nested_key": 1}}}
