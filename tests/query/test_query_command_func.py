"""

    PROJECT: flex_toolbox
    FILENAME: test_query_command_func.py
    AUTHOR: David NAISSE
    DATE: January 03, 2024

    DESCRIPTION: query_command_func function testing
    
"""
import argparse
import json
import os.path
from unittest import TestCase

from src.query import query_command_func
from src.utils import query


class TestQueryCommandFunc(TestCase):

    def test_query_command_func_alias(self):
        # ins
        args = argparse.Namespace()
        args.method = 'GET'
        args.url = 'resources;limit=1'
        args.from_ = 'default'
        args.payload = None

        # outs
        query_command_func(args)

        # test
        assert os.path.isfile("query.json")

        # reset
        os.remove("query.json")

    def test_query_command_func_full_url(self):
        # ins
        args = argparse.Namespace()
        args.method = 'GET'
        args.url = 'https://master.cs-sandbox.flex.cs.dalet.cloud/api/resources;limit=1'
        args.from_ = 'default'
        args.payload = None

        # outs
        query_command_func(args)

        # test
        assert os.path.isfile("query.json")

        # reset
        os.remove("query.json")

    def test_query_command_func_payload_cli(self):
        # ins
        failed_job = query(method='GET', url='jobs;status=Failed;limit=1', log=False).get('jobs')[0]

        args = argparse.Namespace()
        args.method = 'POST'
        args.url = f"jobs/{failed_job.get('id')}/actions"
        args.from_ = 'default'
        args.payload = ['action=retry']

        # outs
        query_command_func(args)

        # test
        assert os.path.isfile("query.json")

        # reset
        os.remove("query.json")

    def test_query_command_func_payload_file(self):
        # ins
        failed_job = query(method='GET', url='jobs;status=Failed;limit=1', log=False).get('jobs')[0]

        args = argparse.Namespace()
        args.method = 'POST'
        args.url = f"jobs/{failed_job.get('id')}/actions"
        args.from_ = 'default'
        args.payload = ['query_config.json']

        with open('query_config.json', 'w') as query_config_file:
            json.dump({'action': 'retry'}, query_config_file)

        # outs
        query_command_func(args)

        # test
        assert os.path.isfile("query_config.json") and os.path.isfile("query.json")

        # reset
        os.remove("query.json")
        os.remove("query_config.json")