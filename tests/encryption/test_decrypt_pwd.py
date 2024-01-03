"""

    PROJECT: flex_toolbox
    FILENAME: test_decrypt_pwd.py.py
    AUTHOR: David NAISSE
    DATE: December 29, 2023

    DESCRIPTION: decrypt_pwd function testing
    
"""
import os
from unittest import TestCase

from src.encryption import encrypt_pwd, decrypt_pwd


class TestEncryptPwd(TestCase):

    def test_decrypt_pwd_valid(self):
        # ins
        pwd = "this is a pwd"

        # outs
        encrypted_pwd = encrypt_pwd(pwd=pwd, key_path=".k")

        # test
        assert decrypt_pwd(pwd=encrypted_pwd, key_path=".k") == pwd

        # clean
        os.remove('.k')

    def test_decrypt_pwd_invalid(self):
        # ins
        pwd = "this is a pwd"
        wrong_pwd = "this is another pwd"

        # outs
        encrypted_pwd = encrypt_pwd(pwd=wrong_pwd, key_path=".k")

        # test
        assert not decrypt_pwd(pwd=encrypted_pwd, key_path=".k") == pwd

        # clean
        os.remove(".k")