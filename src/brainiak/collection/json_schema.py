# -*- coding: utf-8 -*-
from brainiak.utils.links import merge_schemas, pagination_schema, append_param
from brainiak.search.json_schema import SEARCH_PARAM_SCHEMA
from brainiak.schema.get_class import get_cached_schema
from brainiak.prefixes import shorten_uri


def schema(query_params):
    context_name = query_params['context_name']
    class_name = query_params['class_name']
    class_prefix = query_params.get('class_prefix', None)

    if (class_prefix is not None) and query_params.get('expand_uri') == '0':
        class_prefix = shorten_uri(class_prefix)

    args = (context_name, class_name, class_prefix)

    class_schema = get_cached_schema(query_params)

    if class_prefix is not None:
        schema_ref = u"/{0}/{1}/_schema?class_prefix={2}".format(*args)
        href = u"/{0}/{1}?class_prefix={2}".format(*args)
    else:
        schema_ref = u'/{0}/{1}/_schema'.format(*args)
        href = u'/{0}/{1}'.format(*args)

    if 'expand_uri' in query_params:
        expand_uri_param = 'expand_uri={0}'.format(query_params['expand_uri'])
        schema_ref = append_param(schema_ref, expand_uri_param)
        href = append_param(href, expand_uri_param)

    link = build_link(query_params)

    base = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": class_schema.get('title', ''),
        "type": "object",
        "required": ["items", "_class_prefix", "@id"],
        "properties": {
            "_class_prefix": {"type": "string"},
            "pattern": {"type": "string"},  # used in _search service responses
            "do_item_count": {"type": "integer"},
            "item_count": {"type": "integer"},
            "@id": {"type": "string", "format": "uri"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "title": class_schema.get('title', ''),
                    "required": ["title", "@id", "resource_id", "instance_prefix"],
                    "properties": {
                        "title": {"type": "string"},
                        "@id": {"type": "string"},
                        "resource_id": {"type": "string"},
                        "instance_prefix": {"type": "string", "format": "uri"},
                    },
                    "links": [
                        {
                            "href": link,
                            "method": "GET",
                            "rel": "item"
                        },
                        {
                            "href": link,
                            "method": "GET",
                            "rel": "instance"
                        }
                    ]
                }
            },
        },
        "links": [
            {
                "href": "{+_base_url}",
                "method": "GET",
                "rel": "self"
            },
            {
                "href": "{+_schema_url}",
                "method": "GET",
                "rel": "class"
            },
            {
                "href": u"/{0}".format(context_name),
                "method": "GET",
                "rel": "context"
            },
            {
                "href": href,
                "method": "POST",
                "rel": "add",
                "schema": {"$ref": schema_ref}
            },
            {
                "href": "/{0}/{1}/_search?graph_uri={2}&class_uri={3}&pattern={{pattern}}".format(
                        context_name,
                        class_name,
                        query_params['graph_uri'],
                        query_params['class_uri']),
                "method": "GET",
                "rel": "search",
                "schema": SEARCH_PARAM_SCHEMA
            }
        ]
    }

    base_pagination_url = u'/{0}/{1}'.format(context_name, class_name)
    extra_url_params = '&class_prefix={_class_prefix}'
    pagination_dict = pagination_schema(base_pagination_url, extra_url_params)
    merge_schemas(base, pagination_dict)
    return base


def build_link(query_params):
    context_name = query_params['context_name']
    class_name = query_params['class_name']
    expand_uri = query_params.get('expand_uri', None)

    link = u"/{0}/{1}/{{resource_id}}?class_prefix={{class_prefix}}&instance_prefix={{instance_prefix}}".format(context_name, class_name)
    if expand_uri is not None:
        link = append_param(link, 'expand_uri={0}'.format(query_params['expand_uri']))
    return link
