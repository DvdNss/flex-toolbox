"""

    PROJECT: flex_toolbox
    FILENAME: test_connect_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: connect_command_func function testing
    
"""
import argparse
from unittest import TestCase

from src.connect import connect_command_func
from src.encryption import decrypt_pwd
from src.env import get_default_env_alias, get_env


class TestConnectCommandFunc(TestCase):

    def test_connect_command_func_known_full_alias(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'cs-sandbox-ovh-flex-config'
        args.username = None
        args.password = None
        args.alias = None

        # outs
        connect_command_func(args)

        # test
        assert get_default_env_alias() == args.env_url

    def test_connect_command_func_known_partial_alias(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'cs-sandbox-ovh'
        args.username = None
        args.password = None
        args.alias = None

        # outs
        try:
            connect_command_func(args)
            self.fail()
        except:
            pass

    def test_connect_command_func_wrong_alias(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'this-alias-does-not-exist'
        args.username = None
        args.password = None
        args.alias = None

        # outs
        try:
            connect_command_func(args)
            self.fail()
        except:
            pass

    def test_connect_command_func_known_full_url(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'https://master.cs-sandbox.flex.cs.dalet.cloud'
        args.username = None
        args.password = None
        args.alias = None

        # outs
        connect_command_func(args)

        # test
        assert get_default_env_alias() == 'cs-sandbox-ovh-flex-config'

    def test_connect_command_func_known_partial_url(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'cs-sandbox.flex'
        args.username = None
        args.password = None
        args.alias = None

        # out
        try:
            connect_command_func(args)
            self.fail()
        except:
            pass

    def test_connect_command_func_update(self):
        # ins
        env_config = get_env(environment='cs-sandbox-ovh-flex-config')

        args = argparse.Namespace()
        args.env_url = env_config.get('url')
        args.username = env_config.get('username')
        args.password = decrypt_pwd(env_config.get('password'))
        args.alias = None

        # outs
        connect_command_func(args)

        # test
        assert get_default_env_alias() == 'cs-sandbox-ovh-flex-config'

    def test_connect_command_func_new_invalid_url(self):
        # ins
        args = argparse.Namespace()
        args.env_url = 'bad_url'
        args.username = 'bad_username'
        args.password = 'bad_password'
        args.alias = 'bad_alias'

        # outs
        try:
            connect_command_func(args)
            self.fail()
        except:
            # test OK
            pass

    def test_connect_command_func_new_invalid_password(self):
        # ins
        env_config = get_env(environment='cs-sandbox-ovh-flex-config')

        args = argparse.Namespace()
        args.env_url = env_config.get('url')
        args.username = env_config.get('username')
        args.password = 'bad_password'
        args.alias = None

        # outs
        try:
            connect_command_func(args)
            self.fail()
        except Exception as e:
            assert "Authentication details are found invalid" in str(e)
