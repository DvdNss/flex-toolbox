"""

    PROJECT: flex_toolbox
    FILENAME: test_push_command_func.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: push_command_func function testing
    
"""
import argparse
import os.path
import shutil
from unittest import TestCase

from src.pull import pull_command_func
from src.push import push_command_func
from src.utils import query


class TestPushCommandFunc(TestCase):

    def test_push_command_func_actions_with_jars_and_imports(self):
        # ins
        pull_args = argparse.Namespace()
        pull_args.config_item = 'actions'
        pull_args.filters = ['name=ftbx-action-dnaisse']
        pull_args.post_filters = []
        pull_args.from_ = ['cs-sandbox-ovh-flex-config']
        pull_args.with_dependencies = False
        pull_command_func(pull_args)

        # ins
        push_args = argparse.Namespace()
        push_args.config_item = 'actions'
        push_args.item_names = ['ftbx-action-dnaisse']
        push_args.from_ = 'cs-sandbox-ovh-flex-config'
        push_args.to = ['cs-sandbox-ovh-flex-config']
        push_args.retry = False
        push_args.push_to_failed_jobs = None
        push_command_func(push_args)

        # test
        assert os.path.isdir('cs-sandbox-ovh-flex-config') and os.path.isfile(
            os.path.join('cs-sandbox-ovh-flex-config', 'actions', 'ftbx-action-dnaisse', 'jars.json'))

        # reset
        shutil.rmtree('cs-sandbox-ovh-flex-config', ignore_errors=False, onerror=None)

    def test_push_command_func_assets_metadata(self):
        # ins
        pull_args = argparse.Namespace()
        pull_args.config_item = 'assets'
        pull_args.filters = ['id=818']
        pull_args.post_filters = []
        pull_args.from_ = ['cs-sandbox-ovh-flex-config']
        pull_args.with_dependencies = False
        pull_command_func(pull_args)

        # ins
        push_args = argparse.Namespace()
        push_args.config_item = 'assets'
        push_args.item_names = ['818']
        push_args.from_ = 'cs-sandbox-ovh-flex-config'
        push_args.to = ['cs-sandbox-ovh-flex-config']
        push_args.retry = False

        push_args.push_to_failed_jobs = None
        push_command_func(push_args)

        # test
        assert os.path.isdir('cs-sandbox-ovh-flex-config')

        # reset
        shutil.rmtree('cs-sandbox-ovh-flex-config', ignore_errors=False, onerror=None)

    def test_push_command_func_new_actions(self):
        # ins
        pull_args = argparse.Namespace()
        pull_args.config_item = 'actions'
        pull_args.filters = ['name=ftbx-action-dnaisse']
        pull_args.post_filters = []
        pull_args.from_ = ['cs-sandbox-ovh-flex-config']
        pull_args.with_dependencies = False
        pull_command_func(pull_args)

        # ins
        push_args = argparse.Namespace()
        push_args.config_item = 'actions'
        push_args.item_names = ['ftbx-action-dnaisse']
        push_args.from_ = 'cs-sandbox-ovh-flex-config'
        push_args.to = ['devstaging.flex.daletdemos.com']
        push_args.retry = False
        push_args.push_to_failed_jobs = None
        push_command_func(push_args)

        # test
        assert os.path.isdir('cs-sandbox-ovh-flex-config') and os.path.isdir('devstaging.flex.daletdemos.com')

        # reset
        ftbx_action = query(method='GET', url='actions;name=ftbx-action-dnaisse;exactNameMatch=true',
                            environment="devstaging.flex.daletdemos.com")
        ftbx_action_id = ftbx_action.get('actions')[0].get('id')
        query(method="POST", url=f"actions/{ftbx_action_id}/actions", payload={'action': 'disable'},
              environment="devstaging.flex.daletdemos.com")
        query(method="POST", url=f"actions/{ftbx_action_id}/actions", payload={'action': 'delete'},
              environment="devstaging.flex.daletdemos.com")

        shutil.rmtree('cs-sandbox-ovh-flex-config', ignore_errors=False, onerror=None)
        shutil.rmtree('devstaging.flex.daletdemos.com', ignore_errors=False, onerror=None)

    def test_push_command_func_tasks_status(self):
        # ins
        task = query(method='GET', url='tasks;name=task;limit=1')
        task_id = task.get('tasks')[0].get('id')

        pull_args = argparse.Namespace()
        pull_args.config_item = 'tasks'
        pull_args.filters = [f'id={task_id}']
        pull_args.post_filters = []
        pull_args.from_ = ['cs-sandbox-ovh-flex-config']
        pull_args.with_dependencies = False
        pull_command_func(pull_args)

        push_args = argparse.Namespace()
        push_args.config_item = 'tasks'
        push_args.item_names = [f"{task_id}"]
        push_args.from_ = 'cs-sandbox-ovh-flex-config'
        push_args.to = ['cs-sandbox-ovh-flex-config']
        push_args.retry = False
        push_args.push_to_failed_jobs = None

        try:
            push_command_func(push_args)
            self.fail()
        except Exception as e:
            # test
            assert "already completed" in str(e)

        # reset
        shutil.rmtree('cs-sandbox-ovh-flex-config', ignore_errors=False, onerror=None)
