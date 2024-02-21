"""

    PROJECT: flex_toolbox
    FILENAME: test_get_items.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_items function testing
    
"""
from unittest import TestCase

import VARIABLES
from src.utils import get_items


class TestGetItems(TestCase):

    def test_get_items_accounts(self):
        # ins
        config_item = "accounts"
        filters = ['name=Master Account']
        sub_items = VARIABLES.ACCOUNTS_SUB_ITEMS

        # outs
        items = get_items(config_item=config_item, filters=filters, sub_items=sub_items, log=False,
                          environment='cs-sandbox-ovh-flex-config')

        # test
        assert items and items[next(iter(items), {})].get('name') == "Master Account" and \
               all(items[next(iter(items), {})].get(sub_item) for sub_item in VARIABLES.ACCOUNTS_SUB_ITEMS)

    def test_get_items_fql(self):
        # ins
        config_item = "assets"
        filters = ['fql=(name=test)']

        # outs
        items = get_items(config_item=config_item, filters=filters, log=False,
                          environment='cs-sandbox-ovh-flex-config')

        # test
        assert items and 'test' in items[next(iter(items), {})].get("name")

    def test_get_items_limit(self):
        # ins
        config_item = "actions"
        filters = ['limit=3']

        # outs
        items = get_items(config_item=config_item, filters=filters, log=False,
                          environment='cs-sandbox-ovh-flex-config')

        # test
        assert items and len(items) == 3
