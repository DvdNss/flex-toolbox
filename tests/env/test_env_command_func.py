"""

    PROJECT: flex_toolbox
    FILENAME: test_env_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: env_command_func function testing
    
"""
import argparse
from unittest import TestCase

from src.env import env_command_func


class TestEnvCommandFunc(TestCase):

    def test_env_command_func(self):
        try:
            # outs
            env_command_func(argparse.Namespace())
        except:
            self.fail()
