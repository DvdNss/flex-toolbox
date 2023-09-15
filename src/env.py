"""

    PROJECT: flex_toolbox
    FILENAME: env.py
    AUTHOR: David NAISSE
    DATE: September 13, 2023

    DESCRIPTION: TODO
    
"""
import json


def env_command_func(args):
    """Action on env command. """

    # Log default environment
    default_env = read_environments_json()['environments']['default']
    print(f"Current default environment is {default_env['url']} - user: {default_env['username']}. ")


def add_or_update_environments_json(env, username, password, isDefault: bool = False):
    """
    Add env to enrionments.json

    :param env: env url
    :param username: username
    :param password: password
    :param isDefault: whether the env is default or not
    :return:
    """

    # Read
    with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "r") as environments_file:
        environments = json.load(environments_file)

    # Update
    environments['environments'][env if not isDefault else "default"] = {
        "url": env,
        "username": username,
        "password": password,
    }

    # Save
    with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "w") as environments_file:
        json.dump(environments, environments_file, indent=4)

    return environments['environments'][env if not isDefault else "default"]


def read_environments_json():
    """
    Read or creates the environments.json file.

    :return:
    """

    try:
        # Read existing json
        with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "r") as file:
            environments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with the default content
        environments = {'environments': {}}
        with open("C:\\Users\\dvdna\\PycharmProjects\\flex_toolbox\\environments.json", "w") as file:
            json.dump(environments, file, indent=4)

    return environments


def get_default_env():
    """
    Return default environment.

    :return:
    """

    environments = read_environments_json()

    return environments['environments']['default']
