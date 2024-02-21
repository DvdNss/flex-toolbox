"""

    PROJECT: flex_toolbox
    FILENAME: test_get_full_items.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_full_items function testing
    
"""
from unittest import TestCase

from src.utils import get_full_items


class TestGetFullItems(TestCase):

    def test_get_full_items_accounts(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "accounts", ['limit=1'], [], False

        # outs
        accounts = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(profiles, dict) and (
            profiles.get(list(profiles.keys())[0]).get('objectType').get('name') == 'profile' if len(
                list(profiles.keys())) != 0 else True)

    def test_get_full_items_quotas(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "quotas", ['limit=1'], [], False

        # outs
        quotas = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(quotas, dict) and (
            quotas.get(list(quotas.keys())[0]).get('objectType').get('name') == 'quota' if len(
                list(quotas.keys())) != 0 else True)

    def test_get_full_items_resources(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "resources", ['limit=1'], [], False

        # outs
        resources = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(resources, dict) and (
            resources.get(list(resources.keys())[0]).get('objectType').get('name') == 'resource' if len(
                list(resources.keys())) != 0 else True)

    def test_get_full_items_roles(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "roles", ['limit=1'], [], False

        # outs
        roles = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(roles, dict) and (
            roles.get(list(roles.keys())[0]).get('objectType').get('name') == 'role' if len(
                list(roles.keys())) != 0 else True)

    def test_get_full_items_task_definitions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "taskDefinitions", ['limit=1'], [], False

        # outs
        task_definitions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(task_definitions, dict) and (
            task_definitions.get(list(task_definitions.keys())[0]).get('objectType').get(
                'name') == 'task-definition' if len(list(task_definitions.keys())) != 0 else True)

    def test_get_full_items_tasks(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "tasks", ['limit=1'], [], False

        # outs
        tasks = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(tasks, dict) and (
            tasks.get(list(tasks.keys())[0]).get('objectType').get('name') == 'task' if len(
                list(tasks.keys())) != 0 else True)

    def test_get_full_items_taxonomies(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "taxonomies", ['limit=1'], [], False

        # outs
        taxonomies = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(taxonomies, list) and taxonomies[0].get('childTaxons')

    def test_get_full_items_timed_actions(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "timedActions", ['limit=1'], [], False

        # outs
        timed_actions = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(timed_actions, dict) and (
            timed_actions.get(list(timed_actions.keys())[0]).get('objectType').get('name') == 'timed-action' if len(
                list(timed_actions.keys())) != 0 else True)

    def test_get_full_items_user_defined_object_types(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "userDefinedObjectTypes", [], [], False

        # outs
        user_defined_object_types = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(user_defined_object_types, dict) and (
            user_defined_object_types.get(list(user_defined_object_types.keys())[0]).get('objectType').get(
                'name') == 'user-defined-object-type' if len(list(user_defined_object_types.keys())) != 0 else True)

    def test_get_full_items_users(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "users", ['limit=1'], [], False

        # outs
        users = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(users, dict) and (
            users.get(list(users.keys())[0]).get('objectType').get('name') == 'user' if len(
                list(users.keys())) != 0 else True)

    def test_get_full_items_variants(self):
        # ins
        config_item, filters, post_filters, with_dependencies = "variants", ['limit=1'], [], False

        # outs
        variants = get_full_items(
            config_item=config_item,
            filters=filters,
            post_filters=post_filters,
            with_dependencies=with_dependencies,
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config',
            cmd='list'
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
            log=False,
            environment='cs-sandbox-ovh-flex-config'
        )

        # test
        assert isinstance(workspaces, dict) and (
            workspaces.get(list(workspaces.keys())[0]).get('objectType').get('name') == 'workspace' if len(
                list(workspaces.keys())) != 0 else True)
