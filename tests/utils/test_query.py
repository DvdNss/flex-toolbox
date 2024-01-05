"""

    PROJECT: flex_toolbox
    FILENAME: test_query.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: query function testing
    
"""
from unittest import TestCase

from src.utils import query


class TestQuery(TestCase):

    def test_query_valid(self):
        # ins
        method, url, environment = "GET", "resources;limit=1", "cs-sandbox-ovh-flex-config"

        # outs
        response = query(method=method, url=url, log=False, environment=environment)

        # test
        assert 'resources' in response and len(response['resources']) != 0

    def test_query_invalid(self):
        # ins
        method, url, environment = "GET", "resources;invalid", "cs-sandbox-ovh-flex-config"

        # outs
        try:
            query(method=method, url=url, log=False, environment=environment)

            # test
            self.fail()
        except Exception as ex:
            assert "Error message: " in str(ex) and "invalid" in str(ex)
