"""

    PROJECT: flex_toolbox
    FILENAME: env.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: environment file functions
    
"""
import json

import pandas as pd

import VARIABLES
from src.encryption import encrypt_pwd


def env_command_func(args):
    """Action on env command. """

    # retrieve environments
    environments = read_environments_json()['environments']
    default_environment = environments['default']

    pd.set_option('display.colheader_justify', 'center')

    env_df = pd.DataFrame(columns=['DEFAULT', 'ALIAS', 'URL', 'USERNAME'])
    environments.pop('default')

    print("")

    for env_alias, env_config in environments.items():
        is_default = (default_environment['url'] == env_config['url'])

        env_df.loc[len(env_df)] = {
            "DEFAULT": "X" if is_default else "",
            "ALIAS": env_alias,
            "URL": env_config.get('url'),
            "USERNAME": env_config.get('username'),
        }

    print(env_df.to_string(index=False), "\n")


def add_or_update_environments_json(env, username, password, is_default: bool = False, alias: str = None,
                                    env_file_path: str = VARIABLES.ENV_FILE_PATH,
                                    key_path: str = VARIABLES.KEY_FILE_PATH):
    """
    Add env to enrionments.json

    :param env: env url
    :param username: username
    :param password: password
    :param alias: alias for the env
    :param is_default: whether the env is default or not
    :param env_file_path: env file path
    :param key_path: key path
    :return:
    """

    # read
    environments = read_environments_json(env_file_path=env_file_path)

    # update
    alias = alias if alias else env.replace('https://', '')
    environments['environments'][alias if not is_default else "default"] = {
        "url": env,
        "username": username,
        "password": encrypt_pwd(pwd=password, key_path=key_path) if not is_default else password,
    }

    # save
    with open(env_file_path, "w") as environments_file:
        json.dump(environments, environments_file, indent=4)

    return environments['environments'][alias if not is_default else "default"]


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


def get_default_env_alias(env_file_path: str = VARIABLES.ENV_FILE_PATH):
    """
    Get default env alias.
    """

    environments = read_environments_json(env_file_path=env_file_path)['environments']
    url = environments['default']['url']
    environments.pop("default")

    for env_key, env in environments.items():
        if "url" in env and env["url"] == url:
            return env_key if "https://" not in env_key else env_key.replace('https://', '')
    raise IndexError(f"Cannot find environment with url {url} in environments.json. ")
