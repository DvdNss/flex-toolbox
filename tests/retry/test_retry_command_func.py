"""

    PROJECT: flex_toolbox
    FILENAME: test_retry_command_func.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: retry_command_func function testing
    
"""
import argparse
import json
import os.path
from unittest import TestCase

import pandas as pd

from src.retry import retry_command_func
from src.utils import get_items


class TestRetryCommandFunc(TestCase):

    def test_retry_command_func_jobs_api(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ['limit=1']
        args.file = None

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")

    def test_retry_command_func_jobs_csv(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.file = 'instances_to_be_retried.csv'

        failed_job = get_items(config_item=args.config_item, filters=['status=Failed', 'limit=1'], log=False)
        csv = pd.DataFrame([failed_job[next(iter(failed_job), {})].get('id')], columns=['id'])
        csv.to_csv(args.file)

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")
        os.remove(args.file)

    def test_retry_command_func_jobs_json(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.file = 'instances_to_be_retried.json'

        failed_job = get_items(config_item=args.config_item, filters=['status=Failed', 'limit=1'], log=False)
        with open(args.file, 'a+') as instances_to_be_retried:
            json.dump({"failed_jobs_1": failed_job[next(iter(failed_job), {})]}, instances_to_be_retried)

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")
        os.remove(args.file)

    def test_retry_command_func_workflows_api(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'workflows'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = ['limit=1']
        args.file = None

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")

    def test_retry_command_func_workflows_csv(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'workflows'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.file = 'instances_to_be_retried.csv'

        failed_job = get_items(config_item=args.config_item, filters=['status=Failed', 'limit=1'], log=False)
        csv = pd.DataFrame([failed_job[next(iter(failed_job), {})].get('id')], columns=['id'])
        csv.to_csv(args.file)

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")
        os.remove(args.file)

    def test_retry_command_func_workflows_json(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'workflows'
        args.from_ = 'cs-sandbox-ovh-flex-config'
        args.filters = []
        args.file = 'instances_to_be_retried.json'

        failed_job = get_items(config_item=args.config_item, filters=['status=Failed', 'limit=1'], log=False)
        with open(args.file, 'a+') as instances_to_be_retried:
            json.dump({"failed_jobs_1": failed_job[next(iter(failed_job), {})]}, instances_to_be_retried)

        # outs
        retry_command_func(args=args)

        # test
        assert os.path.isfile('retried_instances.csv')

        # reset
        os.remove("retried_instances.csv")
        os.remove(args.file)
