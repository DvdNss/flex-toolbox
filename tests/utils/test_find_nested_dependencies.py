"""

    PROJECT: flex_toolbox
    FILENAME: test_find_nested_dependencies.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: find_nested_dependencies function testing
    
"""
from unittest import TestCase

from src.utils import find_nested_dependencies


class TestFindNestedDependencies(TestCase):

    def test_find_nested_dependencies(self):
        # ins
        data = {
            "id": 999,
            "nested_1": {
                "id": 111,
                "nested_2": {
                    "id": 222,
                }
            }
        }

        # outs
        dependencies = find_nested_dependencies(data=data)

        # test
        assert dependencies == ['nested_1', 'nested_1.nested_2']
