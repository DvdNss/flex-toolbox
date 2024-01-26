"""

    PROJECT: flex_toolbox
    FILENAME: encryption.py
    AUTHOR: David NAISSE
    DATE: November 27, 2023

    DESCRIPTION: encryption functions

    TEST STATUS: FULLY TESTED
"""
import os

from cryptography.fernet import Fernet

import VARIABLES


def encrypt_pwd(pwd: str, key_path: str = os.path.join(str(os.environ.get('FTBX')), '.k')):
    """
    Encrypt pwd

    TEST STATUS: FULLY TESTED

    :param pwd:
    :param key_path:
    :return:
    """

    # create or load key
    if os.path.isfile(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()  # bytes
    else:
        with open(key_path, "wb") as key_file:
            key = Fernet.generate_key()  # bytes
            key_file.write(key)  # string

    return Fernet(key).encrypt(pwd.encode('utf-8')).decode('utf-8')


def decrypt_pwd(pwd: str, key_path: str = os.path.join(str(os.environ.get('FTBX')), '.k')):
    """
    Decrypt pwd

    TEST STATUS: FULLY TESTED

    :param pwd:
    :param key_path:
    :return:
    """

    key = None

    # create or load key
    if os.path.isfile(key_path):
        with open(key_path, "r") as key_file:
            key = key_file.readlines()[0].encode('utf-8')
    else:
        print("No key file detected. ")
        quit()

    return Fernet(key).decrypt(pwd).decode('utf-8')
