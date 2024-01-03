"""

    PROJECT: flex_toolbox
    FILENAME: test_create_folder.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: create_folder function testing
    
"""
import os.path
from unittest import TestCase

from src.utils import create_folder


class TestCreateFolder(TestCase):

    def test_create_folder_not_exist(self):
        # ins
        folder_name = "test_folder"

        # outs
        folder_created = create_folder(folder_name=folder_name, ignore_error=False)

        # test
        assert folder_created and os.path.isdir(folder_name)

        # reset
        os.rmdir(folder_name)

    def test_create_folder_exists_not_ignore_errors(self):
        # ins
        folder_name = "test_folder"

        # outs
        os.mkdir(folder_name)
        folder_created = create_folder(folder_name=folder_name, ignore_error=False)

        # test
        assert not folder_created and os.path.isdir(folder_name)

        # reset
        os.rmdir(folder_name)

    def test_create_folder_exists_ignore_errors(self):
        # ins
        folder_name = "test_folder"

        # outs
        os.mkdir(folder_name)
        folder_created = create_folder(folder_name=folder_name, ignore_error=True)

        # test
        assert folder_created and os.path.isdir(folder_name)

        # reset
        os.rmdir(folder_name)
