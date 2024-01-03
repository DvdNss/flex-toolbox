"""

    PROJECT: flex_toolbox
    FILENAME: test_convert_to_native_type.py
    AUTHOR: David NAISSE
    DATE: January 03, 2024

    DESCRIPTION: convert_to_native_type function testing
    
"""
from unittest import TestCase

from src.utils import convert_to_native_type


class TestConvertToNativeType(TestCase):

    def test_convert_to_native_type_int(self):
        # ins
        string = "1999"

        # outs
        value = convert_to_native_type(string=string)

        # test
        assert type(value) == int and value == 1999

    def test_convert_to_native_type_bool(self):
        # ins
        string = "true"

        # outs
        value = convert_to_native_type(string=string)

        # test
        assert type(value) == bool and value

    def test_convert_to_native_type_float(self):
        # ins
        string = "3.1415"

        # outs
        value = convert_to_native_type(string=string)

        # test
        assert type(value) == float and value == 3.1415

    def test_convert_to_native_type_string(self):
        # ins
        string = "some string"

        # outs
        value = convert_to_native_type(string=string)

        # test
        assert type(value) == str and value == "some string"

