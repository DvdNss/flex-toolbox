"""

    PROJECT: flex_toolbox
    FILENAME: test_list_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: list_command_func function testing
    
"""
import argparse
import json
import os.path
import shutil
from unittest import TestCase

from src.list import list_command_func


class TestListCommandFunc(TestCase):

    def test_list_command_func_filters_classic(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ['limit=1']
        args.post_filters = []

        # outs
        filename = list_command_func(args)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv")

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_filters_fql(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ['fql=(name~dnaisse)']
        args.post_filters = []

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and "dnaisse" in actions[
            next(iter(actions), {})].get('name')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_int(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.post_filters = ['concurrentJobsLimit=0']

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and actions[
            next(iter(actions), {})].get('concurrentJobsLimit') == 0

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_bool(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.post_filters = ['enabled=true']

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and actions[
            next(iter(actions), {})].get('enabled') is True

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_string(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.post_filters = ['name~dnaisse']

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and "dnaisse" in actions[
            next(iter(actions), {})].get('name')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_list(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ["status=Completed", "limit=1"]
        args.post_filters = ['history.events[-1].message~completed']

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and "completed" in actions[
            next(iter(actions), {})].get('history').get('events')[-1].get('message')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_text(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ["status=Completed", "limit=1"]
        args.post_filters = ['history[text]~completed']

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            actions = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and "completed" in str(actions[
            next(iter(actions),
                 {})].get(
            'history'))

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_taxonomies(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'taxonomies'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.post_filters = []

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            taxonomies = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and isinstance(taxonomies, list) and \
               taxonomies[0].get('id')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_tags(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'tagCollections'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.post_filters = []

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            tag_collections = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and isinstance(tag_collections, dict) and \
               tag_collections[next(iter(tag_collections), {})].get('id')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)

    def test_list_command_func_adaptive_sub_items(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'workflows'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ['limit=1']
        args.post_filters = []

        # outs
        filename = list_command_func(args)

        with open(f"{filename}.json", 'r') as list_file:
            workflows = json.load(list_file)

        # test
        assert os.path.exists(f"{filename}.json") and os.path.exists(f"{filename}.csv") and isinstance(workflows, dict) and \
               not workflows[next(iter(workflows), {})].get('jobs')

        # reset
        shutil.rmtree('lists', ignore_errors=False, onerror=None)
