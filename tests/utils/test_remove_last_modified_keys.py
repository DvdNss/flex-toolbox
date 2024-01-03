"""

    PROJECT: flex_toolbox
    FILENAME: test_remove_last_modified_keys.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: remove_last_modified function testing
    
"""
from unittest import TestCase

from src.utils import remove_last_modified_keys


class TestRemoveLastModifiedKeys(TestCase):

    def test_remove_last_modified_keys(self):
        # ins
        dict = {
            "key1": 1,
            "key2": 2,
            "key3": "test",
            "lastModified": "30 Dec 2023 00:00:00"
        }

        # outs
        remove_last_modified_keys(dict)

        # test
        assert dict == {
            "key1": 1,
            "key2": 2,
            "key3": "test",
        }
