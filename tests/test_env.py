"""

    PROJECT: flex_toolbox
    FILENAME: test_env.py
    AUTHOR: David NAISSE
    DATE: November 13, 2023

    DESCRIPTION: TODO
    
"""
import json
import os
from unittest import TestCase

from src.env import add_or_update_environments_json, read_environments_json


class TestEnv(TestCase):
    def test_add_or_update_environments_json_add(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="environments.json")

        # tests
        assert test_add == {"username": username, "password": password, "url": env}

        # reset state
        os.remove("environments.json")

    def test_add_or_update_environments_json_update(self):
        # ins
        env, username, password, is_default = "&pyUnitUpdate", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="environments.json")
        test_update = add_or_update_environments_json(env=env, username=username, password=password + "u",
                                                      is_default=is_default,
                                                      env_file_path="environments.json")

        # tests
        assert test_add == {"username": username, "password": password, "url": env}
        assert test_update == {"username": username, "password": password + "u", "url": env}

        # reset state
        os.remove("environments.json")

    def test_read_environments_json_exist(self):
        # ins
        env_file_path = "environments.json"
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
        env_file_path = "environments.json"

        # outs
        test_read_exist = read_environments_json(env_file_path=env_file_path)

        # test
        assert test_read_exist == {'environments': {}}

        # reset state
        os.remove(env_file_path)
