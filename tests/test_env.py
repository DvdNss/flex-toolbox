"""

    PROJECT: flex_toolbox
    FILENAME: test_env.py
    AUTHOR: David NAISSE
    DATE: November 13, 2023

    DESCRIPTION: tests for env.py
    
"""
import json
import os
from unittest import TestCase

from src.env import add_or_update_environments_json, read_environments_json, get_default_env_alias


class TestEnv(TestCase):
    def test_add_or_update_environments_json_add(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="tmp_environments.json")

        # tests
        assert test_add == {"username": username, "password": password, "url": env}

        # reset state
        os.remove("tmp_environments.json")

    def test_add_or_update_environments_json_update(self):
        # ins
        env, username, password, is_default = "&pyUnitUpdate", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="tmp_environments.json")
        test_update = add_or_update_environments_json(env=env, username=username, password=password + "u",
                                                      is_default=is_default,
                                                      env_file_path="tmp_environments.json")

        # tests
        assert test_add == {"username": username, "password": password, "url": env}
        assert test_update == {"username": username, "password": password + "u", "url": env}

        # reset state
        os.remove("tmp_environments.json")

    def test_read_environments_json_exist(self):
        # ins
        env_file_path = "tmp_environments.json"
        environments = {'environments': {}}

        # outs
        with open(env_file_path, "w") as file:
            json.dump(environments, file, indent=4)

        test_read_exist = read_environments_json(env_file_path=env_file_path)

        # test
        assert test_read_exist == {'environments': {}}

        # reset state
        os.remove(env_file_path)

    def test_read_environments_json_not_exist(self):
        # ins
        env_file_path = "tmp_environments.json"

        # outs
        test_read_exist = read_environments_json(env_file_path=env_file_path)

        # test
        assert test_read_exist == {'environments': {}}

        # reset state
        os.remove(env_file_path)

    def test_get_default_env_alias_valid(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False
        def_env, def_username, def_password, def_is_default = "&pyUnitAdd", "xxx", "xxx", True

        # outs
        test_add_env = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default, env_file_path="tmp_environments.json")
        add_or_update_environments_json(env=def_env, username=def_username, password=def_password, is_default=def_is_default, env_file_path="tmp_environments.json")

        # tests
        assert test_add_env == {"username": username, "password": password, "url": env}
        try:
            env_alias = get_default_env_alias(env_file_path="tmp_environments.json")
            assert env_alias == env
        except:
            self.fail()

        # reset state
        os.remove("tmp_environments.json")

    def test_get_default_env_alias_invalid(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False
        def_env, def_username, def_password, def_is_default = "&pyUnitAdd2", "xxx", "xxx", True

        # outs
        test_add_env = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default, env_file_path="tmp_environments.json")
        add_or_update_environments_json(env=def_env, username=def_username, password=def_password, is_default=def_is_default, env_file_path="tmp_environments.json")

        # tests
        assert test_add_env == {"username": username, "password": password, "url": env}
        try:
            get_default_env_alias(env_file_path="tmp_environments.json")
            self.fail()
        except IndexError:
            pass

        # reset state
        os.remove("tmp_environments.json")