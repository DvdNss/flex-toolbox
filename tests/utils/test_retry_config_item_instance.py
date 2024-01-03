"""

    PROJECT: flex_toolbox
    FILENAME: test_retry_config_item_instance.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: retry_config_item_instance function testing
    
"""
from unittest import TestCase

from src.utils import retry_config_item_instance


class TestRetryConfigItemInstance(TestCase):

    def test_retry_config_item_instance_valid(self):
        # ins
        config_item = "jobs"
        id = 1213

        # outs
        name, progress = retry_config_item_instance(config_item=config_item, id=id)

        # test
        assert name and progress == 0

    def test_retry_config_item_instance_invalid(self):
        # ins
        config_item = "jobs"
        id = 1218

        # outs
        try:
            name, progress = retry_config_item_instance(config_item=config_item, id=id)
        except Exception as e:
            # test
            assert "retry is not available" in str(e)
