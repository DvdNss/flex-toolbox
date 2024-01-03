"""

    PROJECT: flex_toolbox
    FILENAME: test_add_or_update_environments_json.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: test_add_or_update_environments_json function testing
    
"""
import os
from unittest import TestCase

from src.encryption import decrypt_pwd
from src.env import add_or_update_environments_json


class TestAddOrUpdateEnvironmentsJson(TestCase):

    def test_add_or_update_environments_json_add(self):
        # ins
        env, username, password, is_default = "&pyUnitAdd", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="tmp_environments.json", key_path=".k")

        # tests
        test_add['password'] = decrypt_pwd(pwd=test_add.get('password'), key_path=".k")
        assert test_add == {"username": username, "password": password, "url": env}

        # reset state
        os.remove("tmp_environments.json")
        os.remove(".k")

    def test_add_or_update_environments_json_update(self):
        # ins
        env, username, password, is_default = "&pyUnitUpdate", "xxx", "xxx", False

        # outs
        test_add = add_or_update_environments_json(env=env, username=username, password=password, is_default=is_default,
                                                   env_file_path="tmp_environments.json", key_path=".k")
        test_update = add_or_update_environments_json(env=env, username=username, password=password + "u",
                                                      is_default=is_default,
                                                      env_file_path="tmp_environments.json", key_path=".k")

        # tests
        test_add['password'] = decrypt_pwd(pwd=test_add.get('password'), key_path=".k")
        test_update['password'] = decrypt_pwd(pwd=test_update.get('password'), key_path=".k")
        assert test_add == {"username": username, "password": password, "url": env}
        assert test_update == {"username": username, "password": password + "u", "url": env}

        # reset state
        os.remove("tmp_environments.json")
        os.remove(".k")
