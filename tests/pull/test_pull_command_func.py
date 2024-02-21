"""

    PROJECT: flex_toolbox
    FILENAME: test_pull_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: pull_command_func function testing
    
"""
import argparse
import os
import shutil
from unittest import TestCase

from src.pull import pull_command_func


class TestPullCommandFunc(TestCase):

    def test_pull_command_func_jef_script_with_imports_and_jars(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse', 'limit=1']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse')) and \
               os.path.isfile(
                   os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse', 'jars.json')) and os.path.isfile(
            os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse', 'script.groovy'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_envs(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse', 'limit=1']
        args.from_ = ['default', 'cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_filters_classic(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse', 'limit=1']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_filters_fql(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['fql=(name~dnaisse)']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_with_dependencies(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'workflowDefinitions'
        args.filters = ['name=launch-task']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = True
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(
            os.path.join(env_alias, 'taskDefinitions', 'task')) and os.path.isdir(
            os.path.join(env_alias, 'workflowDefinitions', 'launch-task'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_int(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = ['concurrentJobsLimit=0']
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_list(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.filters = ['status=Completed', 'limit=1']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = ['history.events[0]~completed']
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'jobs'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_bool(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = ['enabled=True']
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_string(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = ['name=ftbx-action-dnaisse']
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_text(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.filters = ['name=ftbx-action-dnaisse']
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = ['configuration.instance[text]~execute()']
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)

    def test_pull_command_func_all(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'all'
        args.filters = []
        args.from_ = ['cs-sandbox-ovh-flex-config']
        args.post_filters = []
        args.with_dependencies = False
        env_alias = "cs-sandbox-ovh-flex-config"

        # outs
        pull_command_func(args)

        # test
        assert os.path.isdir(env_alias) and os.path.isdir(
            os.path.join(env_alias, 'actions', 'ftbx-action-dnaisse')) and os.path.isdir(
            os.path.join(env_alias, 'taxonomies')) and os.path.isdir(os.path.join(env_alias, 'workspaces'))

        # reset
        shutil.rmtree(env_alias, ignore_errors=False, onerror=None)
