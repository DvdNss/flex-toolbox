"""

    PROJECT: flex_toolbox
    FILENAME: test_dig_for_tags_and_taxonomies.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: dig_for_tags_and_taxonomies function testing
    
"""
from unittest import TestCase

from src.utils import dig_for_tags_and_taxonomies


class TestDigForTagsAndTaxonomies(TestCase):

    def test_get_tags_and_taxonomies_tags(self):
        # ins
        tags = []
        entries = [
            # depth = 1
            {
                "backingStoreType": "USER_DEFINED_TAG_COLLECTION",
                "backingStoreInstanceId": 7465,
            },
            # depth > 1
            {
                "children":
                    [
                        {
                            "backingStoreType": "USER_DEFINED_TAG_COLLECTION",
                            "backingStoreInstanceId": 74650,
                        },
                    ]

            }
        ]

        # outs
        dig_for_tags_and_taxonomies(entries=entries, tags=tags, taxonomies=[])

        # test
        assert tags == [7465, 74650]

    def test_get_tags_and_taxonomies_taxonomies(self):
        # ins
        taxonomies = []
        entries = [
            # depth =1
            {
                "backingStoreType": "TAXONOMY",
                "filter": "000",
            },
            # depth > 1
            {
                "children":
                    [
                        {
                            "backingStoreType": "TAXONOMY",
                            "filter": "001",
                        },
                    ]

            }
        ]

        # outs
        dig_for_tags_and_taxonomies(entries=entries, tags=[], taxonomies=taxonomies)

        # test
        assert taxonomies == ["000", "001"]
