"""

    PROJECT: flex_toolbox
    FILENAME: query.py
    AUTHOR: David NAISSE
    DATE: October 11, 2023

    DESCRIPTION: query command functions
    
"""

import json

import requests

from src.utils import query

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def query_command_func(args):
    """Action on restore command. """

    # get payload if needed
    if args.payload:
        with open(args.payload, 'r') as payload_file:
            payload = json.load(payload_file)
    else:
        payload = None

    # query
    query_result = query(method=args.method, url=args.url, payload=payload, environment=args.env)

    # save
    with open("query.json", "w") as query_result_file:
        json.dump(query_result, query_result_file, indent=4)
        print("Result of the query has been saved in query.json for your best convenience. \n")

