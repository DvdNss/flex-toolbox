"""

    PROJECT: flex_toolbox
    FILENAME: test_get_auth_material.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: get_auth_material function testing
    
"""
from unittest import TestCase

from src.utils import get_auth_material


class TestGetAuthMaterial(TestCase):

    def test_get_auth_material_valid(self):
        # ins
        environment = "cs-sandbox-ovh-flex-config"

        # outs
        try:
            get_auth_material(environment=environment)
        except:
            self.fail()

    def test_get_auth_material_invalid(self):
        # ins
        environments = "invalid"

        # outs
        try:
            get_auth_material(environment=environments)
            self.fail()
        except KeyError as ke:
            assert "invalid" in str(ke)
