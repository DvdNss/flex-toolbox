"""

    PROJECT: flex_toolbox
    FILENAME: test_compare_command_func.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: compare_command_func function testing
    
"""
import argparse
import os.path
from unittest import TestCase

from src.compare import compare_command_func


class TestCompareCommandFunc(TestCase):

    def test_compare_command_func_valid(self):
        # ins
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.environments = ['cs-sandbox-ovh-flex-config', 'default']
        args.filters = ['name=ftbx-action-dnaisse']

        # outs
        compare_command_func(args)

        # test
        assert os.path.isdir('compare') and os.path.isfile('compare.json')

        # reset
        os.remove('compare.json')

    def test_compare_command_func_invalid(self):
        args = argparse.Namespace()
        args.config_item = 'actions'
        args.environments = ['cs-sandbox-ovh-flex-config']
        args.filters = ['name=ftbx-action-dnaisse']

        # outs
        compare_command_func(args)

        # test
        assert not (os.path.isdir('compare') and os.path.isfile('compare.json'))
