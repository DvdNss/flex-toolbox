"""

    PROJECT: flex_toolbox
    FILENAME: test_reformat_spaces.py
    AUTHOR: David NAISSE
    DATE: December 29, 2023

    DESCRIPTION: reformat_spaces function testing
    
"""

import re
from unittest import TestCase

from src.utils import reformat_spaces


class TestReformatSpaces(TestCase):

    def test_reformat_spaces_single(self):
        # ins
        string = "This is a string with a long space_indent    and then some code. "

        # outs
        reformatted_string = re.sub(r' {4,}', reformat_spaces, string)

        # test
        assert reformatted_string == "This is a string with a long space_indentand then some code. "

    def test_reformat_spaces_multiple(self):
        # ins
        string = "This is a string with multiple space_indent            and then some code. "

        # outs
        reformatted_string = re.sub(r' {4,}', reformat_spaces, string)

        # test
        assert reformatted_string == "This is a string with multiple space_indent        and then some code. "
