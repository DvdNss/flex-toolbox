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

    TEST STATUS: FULLY TESTED

    :param args:
    :return:
    """

    current_dir_options = ['flex_toolbox', 'flex-toolbox', 'flex-toolbox\\', 'flex-toolbox/']

    # get os
    user_os = platform.system()
    print(f"\nOS: {user_os.upper()}\n")

    # get current dir
    current_dir = os.getcwd()
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
                subprocess.run(['setx', 'FTBX', f'{current_dir}'], stdout=subprocess.DEVNULL)
                # .bat
                bat_content = f"@echo off\npython {current_dir}\\ftbx.py %*"
                bat_file_path = 'ftbx.bat'
                with open(bat_file_path, 'w') as bat_file:
                    bat_file.write(bat_content)
            # linux/macOS
            elif user_os in ['Linux', 'Darwin']:
                shell = os.path.basename(os.environ['SHELL'])
                if shell in ['bash', 'zsh']:
                    alias_command = f"alias ftbx='python3 {os.path.expanduser(os.path.join(current_dir, 'ftbx.py'))}'"
                    export_command = f"export FTBX='{os.path.expanduser(current_dir)}'"
                else:
                    print(f"This shell is not supported: {shell}.")
                    quit()
                config_file = os.path.expanduser(f'~/.{shell}rc')
                with open(config_file, 'a') as shell_file:
                    shell_file.write(alias_command + '\n')
                    shell_file.write(export_command + '\n')

            print(
                f"Environment variable FTBX has been set to {current_dir}.\n/!\\ Please close this terminal and open another one. /!\\ \n")
        else:
            print("You must be in the flex_toolbox directory to run this command. ")
    else:
        print("FTBX environment variable already exists, you are good to go!\n")
