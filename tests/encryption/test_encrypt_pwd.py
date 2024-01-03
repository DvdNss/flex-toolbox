"""

    PROJECT: flex_toolbox
    FILENAME: test_encrypt_pwd.py
    AUTHOR: David NAISSE
    DATE: December 29, 2023

    DESCRIPTION: encrypt_pwd function testing
    
"""
import os
from unittest import TestCase

from src.encryption import encrypt_pwd


class TestEncryptPwd(TestCase):

    def test_encrypt_pwd(self):
        # ins
        pwd = "this is a pwd"

        # outs
        encrypted_pwd = encrypt_pwd(pwd=pwd, key_path=".k")

        # test
        assert encrypted_pwd != pwd

        # clean
        os.remove('.k')
