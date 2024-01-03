"""

    PROJECT: flex_toolbox
    FILENAME: test_kebab_to_camel_case.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: kebab_to_camel_case function testing
    
"""
from unittest import TestCase

from src.utils import kebab_to_camel_case


class TestKebabToCamelCase(TestCase):

    def test_kebab_to_camel_case(self):
        # ins
        input = "event-handler"

        # outs
        output = kebab_to_camel_case(input)

        # test
        assert output == "eventHandlers", f"Should be eventHandlers, is {input}."
