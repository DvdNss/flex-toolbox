"""

    PROJECT: flex_toolbox
    FILENAME: env.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: environment file functions
    
"""
import json

import VARIABLES


def env_command_func(args):
    """Action on env command. """

    # log default environment
    default_env = read_environments_json()['environments']['default']
    print(f"Current default environment is {default_env['url']} - user: {default_env['username']}. ")


def add_or_update_environments_json(env, username, password, is_default: bool = False,
                                    env_file_path: str = VARIABLES.ENV_FILE_PATH):
    """
    Add env to enrionments.json

    :param env: env url
    :param username: username
    :param password: password
    :param is_default: whether the env is default or not
    :param env_file_path: env file path
    :return:
    """

    # read
    environments = read_environments_json(env_file_path=env_file_path)

    # update
    environments['environments'][env if not is_default else "default"] = {
        "url": env,
        "username": username,
        "password": password,
    }

    # save
    with open(env_file_path, "w") as environments_file:
        json.dump(environments, environments_file, indent=4)

    return environments['environments'][env if not is_default else "default"]


def read_environments_json(env_file_path: str = VARIABLES.ENV_FILE_PATH):
    """
    Read or creates the environments.json file.

    :param env_file_path: env file path

    :return:
    """

    try:
        # read existing json
        with open(env_file_path, "r") as file:
            environments = json.load(file)
    except FileNotFoundError:
        # if the file doesn't exist, create it with the default content
        environments = {'environments': {}}
        with open(env_file_path, "w") as file:
            json.dump(environments, file, indent=4)

    return environments


def get_env(environment: str = "default"):
    """
    Return default environment.

    :param environment: environment to get from config

    :return:
    """

    environments = read_environments_json()

    return environments['environments'][environment]
