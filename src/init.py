"""

    PROJECT: flex_toolbox
    FILENAME: init.py
    AUTHOR: David NAISSE
    DATE: December 15, 2023

    DESCRIPTION: init command functions

    TEST STATUS: FULLY TESTED
"""

import os
import platform
import subprocess


def init_command_func(args):
    """
    Action on init command.

    TEST STATUS: TODO

    :param args:
    :return:
    """

    current_dir_options = ['flex_toolbox', 'flex-toolbox', 'flex-toolbox\\', 'flex-toolbox/']

    # get os
    user_os = platform.system()
    print(f"\nOS: {user_os.upper()}\n")

    # get current dir
    current_dir = os.path.expanduser(os.getcwd())
    print(f"Current dir: {current_dir} \n")

    # try to get FTBX
    ftbx = os.environ.get('FTBX')

    # FTBX env var doesn't exist
    if not ftbx:
        # check curdir = ftbx dir
        if any(current_dir.endswith(opt) for opt in current_dir_options) or current_dir.endswith(
                "flex-env-config-deploy"):
            # windows
            if user_os == "Windows":
                # permanent
                subprocess.run(['setx', 'FTBX', f'{current_dir}'], stdout=subprocess.DEVNULL)
                # current session
                os.environ['FTBX'] = current_dir
                # .bat
                bat_content = f"@echo off\npython {current_dir}\\ftbx.py %*"
                bat_file_path = 'ftbx.bat'
                with open(bat_file_path, 'w') as bat_file:
                    bat_file.write(bat_content)
            # linux/macOS
            elif user_os in ['Linux', 'Darwin']:
                # permanent - assuming Bash shell for Linux and macOS
                config_file = os.path.expanduser('~/.bashrc')
                with open(config_file, 'a') as file:
                    file.write(f'\nexport FTBX="{current_dir}"\n')
                # current session
                os.environ['FTBX'] = current_dir

            print(
                f"Environment variable FTBX has been set to {current_dir}. Please close this terminal and open another one.\n")
        else:
            print("You must be in the flex_toolbox directory to run this command. ")
    else:
        print("FTBX environment variable already exists, skipping...\n")
