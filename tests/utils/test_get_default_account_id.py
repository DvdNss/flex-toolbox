"""

    PROJECT: flex_toolbox
    FILENAME: test_get_default_account_id.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: get_default_account_id function testing
    
"""
from unittest import TestCase

from src.utils import get_default_account_id


class TestGetDefaultAccountId(TestCase):

    def test_get_default_account_id_valid(self):
        # ins
        environment = 'cs-sandbox-ovh-flex-config'

        # outs
        acccount_id = get_default_account_id(environment=environment)

        # test
        assert isinstance(acccount_id, int)

    def test_get_default_account_id_invalid(self):
        # ins
        environment = 'fake_environment'

        # outs & test
        try:
            account_id = get_default_account_id(environment=environment)
            self.fail()
        except:
            pass
