"""

    PROJECT: flex_toolbox
    FILENAME: test_get_nested_value.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_nested_value function testing
    
"""
from unittest import TestCase

from src.utils import get_nested_value


class TestGetNestedValue(TestCase):

    def test_get_nested_value_valid(self):
        # ins
        data = {
            "nested_1": {
                "nested_2": {
                    "key": "value"
                }
            }
        }

        # outs
        nested_value = get_nested_value(obj=data, keys="nested_1.nested_2.key")

        # test
        assert nested_value == "value"

    def test_get_nested_value_text(self):
        # ins
        data = {
            "nested_1": {
                "nested_2": {
                    "key": "value_as_text"
                }
            }
        }

        # outs
        nested_value = get_nested_value(obj=data, keys="nested_1.nested_2[text]")

        # test
        assert nested_value == "{'key': 'value_as_text'}"

    def test_get_nested_value_list(self):
        # ins
        data = {
            "nested_1": {
                "nested_2": {
                    "items": [
                        {
                            "key": "value_of_list_item_1"
                        },
                        {
                            "key": "value_of_list_item_2"
                        }
                    ]
                }
            }
        }

        # outs
        nested_value = get_nested_value(obj=data, keys="nested_1.nested_2.items[-1].key")

        # test
        assert nested_value == "value_of_list_item_2"

    def test_get_nested_value_invalid(self):
        # ins
        key = "nested_1.nested_2.key"
        data = {
            "nested_1":
                [{
                    "nested_2": {
                        "key": "value"
                    }
                }]
        }

        # outs
        nested_value = get_nested_value(obj=data, keys=key)

        # test
        assert not nested_value
