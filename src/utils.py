"""

    PROJECT: flex_toolbox
    FILENAME: utils.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import os


def create_folder(folder_name: str, ignore_error: bool = False):
    """
    Create folder or return error if already exists.

    :param folder_name: folder name
    :param ignore_error: whether to ignore folder already exists or not

    :return: True if created, False if error
    """

    try:
        os.mkdir(folder_name)
        print(f"Folder {folder_name} was created. ")
        return True
    except FileExistsError:
        if ignore_error:
            return True
        else:
            print(f"Folder {folder_name} already exists. ")
        return False
