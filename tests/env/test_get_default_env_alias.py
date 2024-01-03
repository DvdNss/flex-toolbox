"""

    PROJECT: flex_toolbox
    FILENAME: test_get_default_env_alias.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_default_env_alias function testing
    
"""
import os
from unittest import TestCase

from src.encryption import decrypt_pwd
from src.env import add_or_update_environments_json, get_default_env_alias


class TestGetDefaultEnvAlias(TestCase):

    def test_get_default_env_alias_valid(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False
        def_env, def_username, def_password, def_is_default = "&pyUnitAdd", "xxx", "xxx", True

        # outs
        test_add_env = add_or_update_environments_json(env=env, username=username, password=password,
                                                       is_default=is_default, env_file_path="tmp_environments.json",
                                                       key_path=".k")
        add_or_update_environments_json(env=def_env, username=def_username, password=def_password,
                                        is_default=def_is_default, env_file_path="tmp_environments.json", key_path=".k")

        # tests
        test_add_env['password'] = decrypt_pwd(pwd=test_add_env.get('password'), key_path=".k")
        assert test_add_env == {"username": username, "password": password, "url": env}
        try:
            env_alias = get_default_env_alias(env_file_path="tmp_environments.json")
            assert env_alias == env
        except:
            self.fail()

        # reset state
        os.remove("tmp_environments.json")
        os.remove(".k")

    def test_get_default_env_alias_invalid(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False
        def_env, def_username, def_password, def_is_default = "&pyUnitAdd2", "xxx", "xxx", True

        # outs
        test_add_env = add_or_update_environments_json(env=env, username=username, password=password,
                                                       is_default=is_default, env_file_path="tmp_environments.json",
                                                       key_path=".k")
        add_or_update_environments_json(env=def_env, username=def_username, password=def_password,
                                        is_default=def_is_default, env_file_path="tmp_environments.json", key_path=".k")

        # tests
        test_add_env['password'] = decrypt_pwd(pwd=test_add_env.get('password'), key_path=".k")
        assert test_add_env == {"username": username, "password": password, "url": env}
        try:
            get_default_env_alias(env_file_path="tmp_environments.json")
            self.fail()
        except IndexError:
            pass

        # reset state
        os.remove("tmp_environments.json")
        os.remove(".k")
