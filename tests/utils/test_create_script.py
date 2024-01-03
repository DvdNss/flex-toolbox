"""

    PROJECT: flex_toolbox
    FILENAME: test_create_script.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: create_script function testing
    
"""
import os
from unittest import TestCase

from src.utils import create_script


class TestCreateScript(TestCase):

    def test_create_script(self):
        # ins
        item_name = "pyUnitTest"
        item_config = {
            "configuration": {
                "instance": {
                    "internal-script": {
                        "script-content": "def execute() {\n    context.logInfo('test')\n}",
                        "script-import": [
                            {
                                "value": "groovy.json.JsonSlurper"
                            }
                        ]
                    }
                }
            }
        }

        # outs
        os.mkdir(item_name)
        test_create = create_script(item_name=item_name, item_config=item_config)

        # reset
        os.remove(f"{item_name}/script.groovy")
        os.removedirs(f"{item_name}")

        # test
        expected = "import com.ooyala.flex.plugins.PluginCommand\nimport groovy.json.JsonSlurper\n\nclass Script extends PluginCommand {\n    def execute() {\n        context.logInfo('test')\n    }\n}"
        assert test_create == expected
