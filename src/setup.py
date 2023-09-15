"""

    PROJECT: flex_toolbox
    FILENAME: setup.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import os


def setup_command_func(args):
    """
    Install Flex ToolBox dependencies.

    :param args:
    :return:
    """

    os.system("pip install -r requirements.txt")
