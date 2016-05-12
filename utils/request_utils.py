#!/usr/bin/env python

from api.error import Error
from frameworks.bottle import request, response


def validate_value(name, value, enforced_type=str, max=None, min=None, choices=None, step=None):

    if value is None:
        return None

    # Check type
    try:
        if enforced_type == str:
            value_type = type(value)
            if value_type == unicode:
                value = value.encode("utf-8")
            else:
                value = str(value)
        elif enforced_type == int:
            value = int(value)
        elif enforced_type == bool:
            if type(value) != bool:
                value = value.lower() in ["true"]
        elif enforced_type == float:
            value = float(value)
    except:
        Error.raise_bad_request(response, "Unexpected type {0} for field {1}. Expected {2}.".format(type(value).__name__, name, enforced_type.__name__), field=name)

    # Check step
    if enforced_type == float and step is not None:
        if value % step != 0:
            Error.raise_bad_request(response, "Expected type {0} with incorrect precision for field {1}.".format(type(value).__name__, name), field=name)

    # Check max
    if max:
        if enforced_type == str and len(value) > max or (enforced_type == int or enforced_type == float) and value > max:
            Error.raise_bad_request(response, "Value for field {0} too long. Must be {1} or less.".format(name, max), field=name)

    # Check min
    if min:
        if enforced_type == str and len(value) < min or (enforced_type == int or enforced_type == float) and value < min:
            Error.raise_bad_request(response, "Value for field {0} too short. Must be {1} or more.".format(name, min), field=name)

    # Check choices
    if choices:
        if not value in choices:
            Error.raise_bad_request(response, "Value for field {0} not a valid option.".format(name), field=name)

    return value


def get_values(name, source, enforced_type=str, required=True, max=None, min=None, default=None, choices=None):

    # Get values
    values = None
    if source:
        if source == request.params:
            values = source.getall(name)
        else:
            values = source.get(name)

    # Check default
    if values is None and default is not None:
        values = default

    # Check required
    if required and (values is None or len(values) == 0) :
        Error.raise_bad_request(response, "Missing required field {0}".format(name), field=name)

    # Process values
    processed_values = list()
    if values:
        for value in values:
            processed_values.append(validate_value(name, value, enforced_type=enforced_type, max=max, min=min, choices=choices))

    return processed_values


def get_value(name, source, enforced_type=str, required=True, max=None, min=None, default=None, choices=None, step=None):

    # Get value
    value = source.get(name) if source else None
    if value is None and default is not None:
        value = default

    # Check required
    if value is None and required:
        Error.raise_bad_request(response, "Missing required field {0}".format(name), field=name)

    return validate_value(name, value, enforced_type=enforced_type, max=max, min=min, choices=choices, step=step)
