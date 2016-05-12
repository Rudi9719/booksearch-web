#!/usr/bin/env python

import datetime

from google.appengine.api import search

from frameworks.bottle import request

EXPECTED_PARAM_TYPE_BOOL = "bool"
EXPECTED_PARAM_TYPE_STRING = "string"
EXPECTED_PARAM_TYPE_RANGE = "range"

def get_value_for_field(document, field_name):
    return next((field.value for field in document.fields if field.name == field_name), None)

def query_string_for_field(name, type=EXPECTED_PARAM_TYPE_STRING, value=None, include=True):

    query_string = None

    # Get param
    param_values = None
    if value:
        param_values = [value]
    else:
        param_values = request.params.getall(name)

    # Process param
    if param_values:
        if type == EXPECTED_PARAM_TYPE_STRING:
            param_values = filter(lambda param_value: len(param_value) > 0, param_values)
            if len(param_values) > 0:
                if include:
                    query_string = " OR ".join(map(lambda value: "{0} = \"{1}\"".format(name, value), param_values))
                else:
                    query_string = " AND ".join(map(lambda value: "NOT {0} = \"{1}\"".format(name, value), param_values))
        elif type == EXPECTED_PARAM_TYPE_BOOL:
            query_string = "{0} = {1}".format(name, "1" if param_values[0] == "true" else "0")
        elif type == EXPECTED_PARAM_TYPE_RANGE:
            param_value_split = param_values[0].split("-")
            if len(param_value_split) == 1:
                query_string = "{0} = {1}".format(name, param_value_split[0])
            elif len(param_value_split) == 2:
                query_list = list()
                if param_value_split[0] != "":
                    query_list.append("{0} >= {1}".format(name, param_value_split[0]))
                if param_value_split[1] != "":
                    query_list.append("{0} <= {1}".format(name, param_value_split[1]))
                query_string = " AND ".join(query_list)

    # Get query string
    if query_string:
        query_string = "({0})".format(query_string)

    return query_string

def get_document_field_for_value(field_name, value):

    if value is None:
        return

    document_field = None
    if (type(value) == str or type(value) == unicode) and len(value) > 0:
        document_field = search.AtomField(name=field_name, value=value)
    elif type(value) == int or type(value) == float:
        document_field = search.NumberField(name=field_name, value=value)
    elif type(value) == bool:
        document_field = search.NumberField(name=field_name, value=int(value))
    elif type(value) == list and len(value) > 0:
        document_field = search.TextField(name=field_name, value=" ".join(value))
    elif type(value) == datetime.datetime or type(value) == datetime.date:
        document_field = search.DateField(name=field_name, value=value)

    return document_field
