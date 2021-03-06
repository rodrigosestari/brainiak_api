# -*- coding: utf-8 -*-

import unittest
from brainiak.suggest.json_schema import SUGGEST_PARAM_SCHEMA
from brainiak.root.json_schema import schema as root_schema


class TestRootJsonSchema(unittest.TestCase):

    maxDiff = None

    def test_valid_structure(self):
        computed_schema = root_schema()
        self.assertEqual(type(computed_schema), dict)

    def _test_list_contexts(self):
        computed_schema = root_schema()
        expected_links = [
            {'href': '?{+_first_args}', 'method': 'GET', 'rel': 'first'},
            {'href': '?{+_last_args}', 'method': 'GET', 'rel': 'last'},
            {'href': '?{+_next_args}', 'method': 'GET', 'rel': 'next'},
            {'href': '?{+_previous_args}', 'method': 'GET', 'rel': 'previous'},
            {'href': '{+_base_url}', 'method': 'GET', 'rel': 'self'},
            {
                'href': '/_suggest',
                'method': 'POST',
                'rel': 'suggest',
                'schema': SUGGEST_PARAM_SCHEMA
            },
            {
                'href': '/{{context_id}}/{{collection_id}}',
                'method': 'GET',
                'rel': 'collection',
                'schema': {
                    'properties': {
                        'class_prefix': {'type': 'string'}
                    },
                    'type': 'object'}
            },
            {
                'href': '/{{context_id}}/{{collection_id}}/{{resource_id}}',
                'method': 'GET',
                'rel': 'instance',
                'schema': {
                    'properties': {
                        'class_prefix': {'type': 'string'},
                        'instance_prefix': {'type': 'string'}
                    },
                    'type': 'object'
                }
            }
        ]

        self.assertEqual(sorted(computed_schema["links"]), sorted(expected_links))
