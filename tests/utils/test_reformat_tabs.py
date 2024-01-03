"""

    PROJECT: flex_toolbox
    FILENAME: test_reformat_tabs.py
    AUTHOR: David NAISSE
    DATE: December 29, 2023

    DESCRIPTION: reformat_tabs function testing
    
"""
import re
from unittest import TestCase

from src.utils import reformat_tabs


class TestReformatTabs(TestCase):

    def test_reformat_tabs_single(self):
        # ins
        string = "This is a string with a single \t and then nothing. "

        # outs
        reformatted_string = re.sub(r'\t+', reformat_tabs, string)

        # test
        assert reformatted_string == "This is a string with a single  and then nothing. "

    def test_reformat_tabs_multiple(self):
        # ins
        string = "This is a string with multiple \t\t\t\t and then nothing. "

        # outs
        reformatted_string = re.sub(r'\t+', reformat_tabs, string)

        # test
        assert reformatted_string == "This is a string with multiple \t\t\t and then nothing. "
