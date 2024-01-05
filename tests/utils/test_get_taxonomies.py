"""

    PROJECT: flex_toolbox
    FILENAME: test_get_taxonomies.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_taxonomies function testing
    
"""
from unittest import TestCase

from src.utils import get_taxonomies


class TestGetTaxonomies(TestCase):

    def test_get_taxonomies_valid(self):
        # ins
        filters = ["enabled=true"]

        # outs
        try:
            taxonomies = get_taxonomies(filters=filters, log=False, environment='cs-sandbox-ovh-flex-config')
            assert isinstance(taxonomies, list)
        except:
            self.fail()