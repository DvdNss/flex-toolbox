"""

    PROJECT: flex_toolbox
    FILENAME: test_check_all_x_or_nan.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: check_all_x_or_nan function testing
    
"""

from unittest import TestCase

import numpy as np
import pandas as pd

from src.compare import check_all_x_or_nan


class TestCheckAllXOrNan(TestCase):

    def test_check_all_x_or_nan_valid(self):
        # ins
        values = {
                'env-dev': ['value_1', 'value_2', True, 0],
                'env-stg': ['x', 'x', 'x', 'x'],
                'env-prod': ['x', 'x', None, np.NaN],
            }

        # outs
        df = pd.DataFrame(values)

        # test
        assert check_all_x_or_nan(df)

    def test_check_all_x_or_nan_invalid(self):
        # ins
        values = {
            'env-dev': ['value_1', 'value_2', True, 0],
            'env-stg': ['x', 'x', 'x', 'x'],
            'env-prod': ['x', 'x', None, "this value is not x nor NaN nor None"],
        }

        # outs
        df = pd.DataFrame(values)

        # test
        assert not check_all_x_or_nan(df)
