"""

    PROJECT: flex_toolbox
    FILENAME: test_read_environments_json.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: read_environments_json function testing
    
"""
import json
import os
from unittest import TestCase

from src.env import read_environments_json


class TestReadEnvironmentsJson(TestCase):

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
