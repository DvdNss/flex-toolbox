"""

    PROJECT: flex_toolbox
    FILENAME: test_str_to_bool.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: str_to_bool function testing
    
"""
from unittest import TestCase

from src.utils import str_to_bool


class TestStrToBool(TestCase):

    def test_str_to_bool_true(self):
        # ins
        string = "TRUE"

        # outs
        boolean = str_to_bool(string=string)

        # test
        assert boolean

    def test_str_to_bool_lower_true(self):
        # ins
        string = "FALSE"

        # outs
        boolean = str_to_bool(string=string)

        # test
        assert not boolean
