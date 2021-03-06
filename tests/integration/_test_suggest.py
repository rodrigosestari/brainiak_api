# -*- coding: utf-8 -*-
import json


import urllib

import requests
from estester import ElasticSearchQueryTestCase
from mock import patch

from brainiak.suggest.suggest import QUERY_PREDICATE_RANGES, \
    QUERY_SUBPROPERTIES, _build_class_fields_query, \
    _build_body_query
from brainiak.utils.sparql import filter_values
from brainiak import settings

from tests.sparql import QueryTestCase
from tests.tornado_cases import TornadoAsyncHTTPTestCase


class SuggestIntegrationTestCase(TornadoAsyncHTTPTestCase, QueryTestCase):

    index = "aninalia.sample"
    fixtures = ["tests/sample/animalia.n3"]
    graph_uri = "http://example.onto/"

    maxDiff = None

    VALID_BODY_PARAMS = {
        'search': {
            'pattern': 'york',
            'target': 'http://example.onto/birthPlace'
        }
    }

    def setUp(self):
        super(SuggestIntegrationTestCase, self).setUp()
        # ONLY VALID FOR VALID_BODY_PARAMS
        self.elastic_request_url = "http://" + settings.ELASTICSEARCH_ENDPOINT + "/semantica.example.onto/"
        self.elastic_request_url += urllib.parse.quote_plus("http://example.onto/City") + "/"
        self.elastic_request_url += urllib.parse.quote_plus("http://example.onto/York")
        entry = {
            "http://www.w3.org/2000/01/rdf-schema#label": "York",
            "http://example.onto/nickname": "City of York",
            "http://example.onto/description": "York is a walled city, situated at the confluence of the Rivers Ouse and Foss in North Yorkshire, England."
        }

        requests.put(self.elastic_request_url + "?refresh=true", data=json.dumps(entry))

    def tearDown(self):
        super(SuggestIntegrationTestCase, self).setUp()
        requests.delete(self.elastic_request_url)

    @patch("brainiak.utils.i18n.settings", DEFAULT_LANG="en")
    def test_request_with_invalid_predicate(self, settings):
        INVALID_PARAMS = {
            "search": {
                'pattern': 'york',
                'target': 'http://example.onto/invalidPredicate'
            }
        }
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(INVALID_PARAMS))
        self.assertEqual(response.code, 400)
        expected_error_msg = "HTTP error: 400\nEither the predicate http://example.onto/invalidPredicate does not exists or it does not have any rdfs:range defined in the triplestore"
        json_received = json.loads(response.body)
        self.assertIn(expected_error_msg, json_received['errors'])

    @patch("brainiak.suggest.suggest.safe_slug_to_prefix", return_value="http://example.onto/")
    @patch("brainiak.suggest.suggest.uri_to_slug", return_value="example.onto")
    def test_successful_request(self, mocked_uri_to_slug, mock_safe_slug_to_prefix):
        expected_items = [
            {
                u'@id': u'http://example.onto/York',
                u'title': u'York',
                u'rdfs:label': u'York',
                u'@type': u'http://example.onto/City',
                u'type_title': u'City',
                u'_type_title': u'City'
            }
        ]
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(self.VALID_BODY_PARAMS))
        self.assertEqual(response.code, 200)
        response_json = json.loads(response.body)
        self.assertEqual(expected_items, response_json["items"])

    @patch("brainiak.suggest.suggest.safe_slug_to_prefix", return_value="http://example.onto/")
    @patch("brainiak.suggest.suggest.uri_to_slug", return_value="example.onto")
    def test_successful_request_with_non_default_field(self, mocked_uri_to_slug, mock_safe_slug_to_prefix):
        params = {
            'search': {
                'pattern': 'york',
                'target': 'http://example.onto/birthPlace',
                'fields': ["http://example.onto/description"]
            }
        }
        expected_items = [
            {
                u'@id': u'http://example.onto/York',
                u'title': u'York',
                u'rdfs:label': u'York',
                u'@type': u'http://example.onto/City',
                u'type_title': u'City',
                u'_type_title': u'City'
            }
        ]
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(params))
        self.assertEqual(response.code, 200)
        response_json = json.loads(response.body)
        self.assertEqual(expected_items, response_json["items"])

    @patch("brainiak.suggest.suggest.safe_slug_to_prefix", return_value="http://example.onto/")
    @patch("brainiak.suggest.suggest.uri_to_slug", return_value="example.onto")
    def test_successful_request_with_metafields(self, mocked_uri_to_slug, mock_safe_slug_to_prefix):
        expected_items = [
            {
                u'@id': u'http://example.onto/York',
                u'title': u'York',
                u'rdfs:label': u'York',
                u'@type': u'http://example.onto/City',
                u'type_title': u'City',
                u'_type_title': u'City',
                u"instance_fields": [
                    {
                        u"predicate_id": u"http://example.onto/description",
                        u"predicate_title": u"Description of a place",
                        u"object_title": u"York is a walled city, situated at the confluence of the Rivers Ouse and Foss in North Yorkshire, England.",
                        u"required": False
                    },
                    {
                        u"predicate_id": u"http://example.onto/nickname",
                        u"predicate_title": u"Nickname of a place",
                        u"object_title": u"City of York",
                        u"required": False
                    }
                ]
            }
        ]

        VALID_BODY_PARAMS_WITH_METAFIELDS = dict(self.VALID_BODY_PARAMS)
        VALID_BODY_PARAMS_WITH_METAFIELDS.update({
            "response": {
                "meta_fields": ["http://example.onto/suggestMetaField"]
            }
        })
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(VALID_BODY_PARAMS_WITH_METAFIELDS))
        self.assertEqual(response.code, 200)
        response_json = json.loads(response.body)
        self.assertEqual(expected_items, response_json["items"])

    @patch("brainiak.suggest.suggest.safe_slug_to_prefix", return_value="http://example.onto/")
    @patch("brainiak.suggest.suggest.uri_to_slug", return_value="example.onto")
    def test_zero_results(self, mocked_uri_to_slug, mock_safe_slug_to_prefix):
        zero_results_parameters = {
            "search": {
                "pattern": "non existent keywords",
                "target": "http://example.onto/birthPlace"
            }
        }
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(zero_results_parameters))
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, '{}')

    @patch("brainiak.utils.i18n.settings", DEFAULT_LANG="en")
    def test_suggest_with_invalid_json(self, settings):
        response = self.fetch('/_suggest',
                              method='POST',
                              body="Invalid JSON")
        self.assertEqual(response.code, 400)
        json_received = json.loads(response.body)
        expected_message = "JSON malformed. Received: Invalid JSON"
        self.assertIn(expected_message, json_received['errors'][0])

    def test_suggest_without_required_param_target(self):
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps({'search': {'pattern': 1}}))
        self.assertEqual(response.code, 400)
        json_received = json.loads(response.body)
        self.assertIn("'target' is a required property", json_received['errors'][0])

    def test_suggest_with_invalid_body_param(self):
        d = {'invalid': 3}
        d.update(self.VALID_BODY_PARAMS)
        response = self.fetch('/_suggest',
                              method='POST',
                              body=json.dumps(d))
        self.assertEqual(response.code, 400)
        json_received = json.loads(response.body)
        self.assertIn("Additional properties are not allowed (u'invalid' was unexpected)", json_received['errors'][0])

    def test_query_predicate_superclass_range(self):
        expected_classes = ["http://example.onto/Place", "http://example.onto/City"]
        expected_labels = ["Place", "City"]
        expected_graphs = ["http://example.onto/", "http://example.onto/"]

        query_params = {
            "target": "http://example.onto/birthPlace",
            "lang_filter_range_label": ""
        }
        query_response = self.query(QUERY_PREDICATE_RANGES % query_params)
        response_classes = filter_values(query_response, "range")
        response_labels = filter_values(query_response, "range_label")
        response_graphs = filter_values(query_response, "range_graph")

        self.assertEqual(expected_classes, response_classes)
        self.assertEqual(expected_labels, response_labels)
        self.assertEqual(expected_graphs, response_graphs)

    def test_query_subproperties(self):
        expected = ["http://example.onto/birthCity"]
        params = {
            "ruleset": "http://example.onto/ruleset",
            "property": "http://example.onto/birthPlace"
        }
        query_response = self.query(QUERY_SUBPROPERTIES % params)

        response = filter_values(query_response, "property")
        self.assertEqual(expected, response)

    def test_query_meta_fields(self):
        expected = ["http://example.onto/nickname, http://example.onto/description"]
        classes = ["http://example.onto/City"]
        meta_field = "http://example.onto/suggestMetaField"
        query = _build_class_fields_query(classes, meta_field)
        query_response = self.query(query)
        meta_field_values = filter_values(query_response, "field_value")
        self.assertEqual(expected, meta_field_values)


class SuggestIntegrationElasticSearchComplexQueriesTestCase(ElasticSearchQueryTestCase):
    analyzer = "my_analyzer"
    settings = {
        "analysis": {
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"]
                }
            }
        }
    }
    index = "sports.sample"
    fixtures = [
        {
            "body": {
                "title": "Fluminense x Flamengo"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/175096"
        },
        {
            "body": {
                "title": "Comercial-PI 1 x 0 Flamengo-PI - 17/06/2012 16:00"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/160154"
        },
        {
            "body": {
                "title": "Vasco 2 x 1 Flamengo - 16/10/2002"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24762"
        },
        {
            "body": {
                "title": "Bahia 0 x 2 Flamengo - 19/08/2001 16:00"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24241"
        },
        {
            "body": {
                "title": "Flamengo 1 x 1 Cruzeiro - 01/09/2002"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24624"
        },
        {
            "body": {
                "title": "Atl\\u00e9tico-MG 0 x 3 Flamengo - 22/09/2002"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24696"
        },
        {
            "body": {
                "title": "Flamengo 0 x 0 Fortaleza - 14/05/2006 18:10"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/26488"
        },
        {
            "body": {
                "title": "Flamengo 0 x 2 Santos - 19/04/2003 18:00"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24930"
        },
        {
            "body": {
                "title": "Flamengo 0 x 1 Corinthians - 30/10/2002"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24798"
        },
        {
            "body": {
                "title": "Flamengo 2 x 0 Botafogo - 02/11/2002"
            },
            "type": "sports:Match",
            "id": "http://sports.onto/Match/24809"
        },
        {
            "body": {
                "title": "Flamengo"
            },
            "type": "sports:Team",
            "id": "http://sports.onto/Team/123"
        }
    ]

    def query_by_pattern(self, pattern, fields):
        query_params = {"page": "0"}
        search_params = {
            "pattern": pattern
        }
        classes = ["sports:Match", "sports:Team"]
        search_fields = fields
        response_fields = ["title"]

        query = _build_body_query(query_params, search_params, classes, search_fields, response_fields, self.analyzer)
        return query

    def test_query_returns_team_flamengo_before_matches(self):
        pattern = "flamengo"
        fields = ["title"]
        query = self.query_by_pattern(pattern, fields)
        response = self.search(query)
        self.assertEqual(response["hits"]["total"], 11)
        self.assertEqual(response["hits"]["hits"][0]["_id"], u"http://sports.onto/Team/123")
        self.assertEqual(response["hits"]["hits"][0]["fields"]["title"], u"Flamengo")
