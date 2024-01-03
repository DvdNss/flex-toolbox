"""

    PROJECT: flex_toolbox
    FILENAME: query.py
    AUTHOR: David NAISSE
    DATE: October 11, 2023

    DESCRIPTION: query command functions

    TEST STATUS: FULLY TESTED
    
"""

import json

import requests

from src.utils import query, convert_to_native_type

# global variables
PAYLOAD = ""
HEADERS = {'Content-Type': 'application/vnd.nativ.mio.v1+json'}

# init. session
session = requests.Session()


def query_command_func(args):
    """
    Action on restore command.

    TEST STATUS: FULLY TESTED

    """

    # get payload if needed
    if args.payload:
        # file
        if len(args.payload) == 1 and ".json" in args.payload[0]:
            with open(args.payload[0], 'r') as payload_file:
                payload = json.load(payload_file)
        # command line args
        else:
            payload = dict()
            for param in args.payload:
                key, value = param.split('=')[0], param.split('=')[1]
                payload[key] = convert_to_native_type(value)
    else:
        payload = None

    # query
    query_result = query(method=args.method, url=args.url, payload=payload, environment=args.from_)

    # save
    with open("query.json", "w") as query_result_file:
        json.dump(query_result, query_result_file, indent=4)
        print("Result of the query has been saved in query.json for your best convenience. \n")

