"""

    PROJECT: flex_toolbox
    FILENAME: test_apply_post_retrieval_filters.py
    AUTHOR: David NAISSE
    DATE: December 29, 2023

    DESCRIPTION: apply_post_retrieval_filters function testing
    
"""
from unittest import TestCase

from src.utils import apply_post_retrieval_filters


class TestApplyPostRetrievalFilters(TestCase):

    def test_apply_post_retrieval_filters_int(self):
        # ins
        filters = ['not_nested_key>0', 'nested.nested_key!=0']
        items = {
            "item_1": {
                "not_nested_key": 0,
                "nested": {
                    "nested_key": 0
                }
            },
            "item_2": {
                "not_nested_key": 1,
                "nested": {
                    "nested_key": 1
                }
            }
        }

        # outs
        filtered_items = apply_post_retrieval_filters(items=items, filters=filters, log=False)

        # test
        assert filtered_items == {"item_2": {"not_nested_key": 1, "nested": {"nested_key": 1}}}

    def test_apply_post_retrieval_filters_string(self):
        # ins
        filters = ['not_nested_key=equals', 'nested.nested_key~contain']
        items = {
            "item_1": {
                "not_nested_key": "not_equals",
                "nested": {
                    "nested_key": "contain"
                }
            },
            "item_2": {
                "not_nested_key": "equals",
                "nested": {
                    "nested_key": "contains"
                }
            }
        }

        # outs
        filtered_items = apply_post_retrieval_filters(items=items, filters=filters, log=False)

        # test
        assert filtered_items == {"item_2": {"not_nested_key": "equals", "nested": {"nested_key": "contains"}}}

    def test_apply_post_retrieval_filters_bool(self):
        # ins
        filters = ['not_nested_key=true', 'nested.nested_key=false']
        items = {
            "item_1": {
                "not_nested_key": True,
                "nested": {
                    "nested_key": True
                }
            },
            "item_2": {
                "not_nested_key": True,
                "nested": {
                    "nested_key": False
                }
            }
        }

        # outs
        filtered_items = apply_post_retrieval_filters(items=items, filters=filters, log=False)

        # test
        assert filtered_items == {"item_2": {"not_nested_key": True, "nested": {"nested_key": False}}}

    def test_apply_post_retrieval_filters_list(self):
        # ins
        filters = ['events[-1].nested_key~contains']
        items = {
            "item_1": {
                "not_nested_key": True,
                "nested": {
                    "nested_key": True
                },
                "events": [
                    {
                        "nested_key": "bad value"
                    },
                    {
                        "nested_key": "This string contains contains. "
                    }
                ]
            },
            "item_2": {
                "not_nested_key": True,
                "nested": {
                    "nested_key": False
                },
                "events": [
                    {
                        "nested_key": "bad value"
                    },
                    {
                        "nested_key": "This string doesn't contain the given word. "
                    }
                ]
            }
        }

        # outs
        filtered_items = apply_post_retrieval_filters(items=items, filters=filters, log=False)

        # test
        assert filtered_items == {"item_1": {
            "not_nested_key": True,
            "nested": {
                "nested_key": True
            },
            "events": [
                {
                    "nested_key": "bad value"
                },
                {
                    "nested_key": "This string contains contains. "
                }
            ]
        }}
