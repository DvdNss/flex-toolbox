"""

    PROJECT: flex_toolbox
    FILENAME: test_launch_config_item_instance.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: launch_config_item_instance function testing
    
"""
from time import sleep
from unittest import TestCase

from src.utils import launch_config_item_instance, query


class TestLaunchConfigItemInstance(TestCase):

    def test_launch_config_item_instance_valid(self):
        # ins
        config_item = "jobs"
        payload = {
            'actionId': 410
        }

        # outs
        launched_instance = launch_config_item_instance(config_item=config_item, payload=payload, environment='cs-sandbox-ovh-flex-config')

        # test
        assert launched_instance and launched_instance.get('progress') >= 0

        # reset
        sleep(1)
        query(method="POST", url=f"jobs/{launched_instance.get('id')}/actions", payload={"action": "cancel"}, environment='cs-sandbox-ovh-flex-config')

    def test_launch_config_item_instance_invalid(self):
        # ins
        config_item = "jobs"
        payload = {
            'actionId': 0
        }

        # outs
        try:
            launched_instance = launch_config_item_instance(config_item=config_item, payload=payload, environment='cs-sandbox-ovh-flex-config')
        except Exception as e:
            assert 'does not exist' in str(e)
