"""

    PROJECT: flex_toolbox
    FILENAME: test_launch_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: launch_command_func funciton testing
    
"""
import argparse
import json
import os
from time import sleep
from unittest import TestCase

from src.launch import launch_command_func
from src.utils import query


class TestLaunchCommandFunc(TestCase):

    def test_launch_command_func_valid(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.item_name = 'basic-long-running-action'
        args.in_ = 'cs-sandbox-ovh-flex-config'
        args.params = []
        args.from_file = None
        args.use_local = False

        # outs
        launched_instance = launch_command_func(args)

        # test
        assert launched_instance

        # reset
        sleep(1)
        query(method="POST", url=f"jobs/{launched_instance.get('id')}/actions", payload={"action": "cancel"}, environment='cs-sandbox-ovh-flex-config')

    def test_launch_command_func_invalid(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.item_name = "this action doesn\'t exist"
        args.in_ = 'cs-sandbox-ovh-flex-config'
        args.params = []
        args.from_file = None
        args.use_local = False

        # outs
        try:
            launched_instance = launch_command_func(args)
        except:
            # if we're here it's validated
            pass

    def test_launch_command_func_params_command(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.item_name = 'basic-long-running-action'
        args.in_ = 'cs-sandbox-ovh-flex-config'
        args.params = ['assetId=809']
        args.from_file = None
        args.use_local = False

        # outs
        launched_instance = launch_command_func(args)

        # test
        assert launched_instance

    def test_launch_command_func_params_file(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'jobs'
        args.item_name = 'basic-long-running-action'
        args.in_ = 'cs-sandbox-ovh-flex-config'
        args.params = []
        args.from_file = 'launch_params.json'
        args.use_local = False
        params = {'assetId': 809}

        with open('launch_params.json', 'w+') as launch_params_file:
            json.dump(params, launch_params_file)

        # outs
        launched_instance = launch_command_func(args)

        # test
        assert os.path.isfile('launch_params.json') and launched_instance

        # reset
        sleep(3)
        query(method="POST", url=f"jobs/{launched_instance.get('id')}/actions", payload={"action": "cancel"}, environment='cs-sandbox-ovh-flex-config')
        os.remove('launch_params.json')
