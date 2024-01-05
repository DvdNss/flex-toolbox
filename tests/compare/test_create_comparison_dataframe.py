"""

    PROJECT: flex_toolbox
    FILENAME: test_create_comparison_dataframe.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: create_comparison_dataframe function testing
    
"""

from unittest import TestCase

import pandas as pd

from src.compare import create_comparison_dataframe


class TestCreateComparisonDataframe(TestCase):

    def test_create_comparison_dataframe(self):
        # ins
        comparison_dict = {
            'env-dev': {
                'string': 'value_1',
                'bool': True,
                'int': 0,
                'float': 3.1415,
                'nested': {
                    'nested_string': 'value_2'
                }
            },
            'env-stg': {
                'string': 'value_1',
                'bool': True,
                'int': 0,
                'float': 3.1415,
                'nested': {
                    'nested_string': 'value_2'
                }
            },
            'env-prod': {
                'string': 'value_1_but_wrong',
                'bool': False,
                'int': 1,
                'float': 3.1415,
                'nested': {
                    'nested_string': 'wrong_value'
                }
            }
        }

        expected_dict = {
            'env-dev': {
                'string': 'value_1',
                'bool': True,
                'int': 0,
                'float': 3.1415,
                'nested.nested_string': 'value_2'
            },
            'env-stg': {
                'string': 'x',
                'bool': 'x',
                'int': 'x',
                'float': 'x',
                'nested.nested_string': 'x'
            },
            'env-prod': {
                'string': 'value_1_but_wrong',
                'bool': False,
                'int': 1,
                'float': 'x',
                'nested.nested_string': 'wrong_value'
            }
        }

        # outs
        df = create_comparison_dataframe(comparison_dict=comparison_dict)
        expected_df = create_comparison_dataframe(comparison_dict=expected_dict)

        # test
        assert df.equals(expected_df)
