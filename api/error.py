#!/usr/bin/env python

import httplib
import json
import logging

from frameworks.bottle import HTTPError, TemplateError


class BookSearchError(HTTPError):

    def __init__(self, status, code, message, field=None):
        body_json = {
            "valid": False,
            "code": code,
            "message": message
        }
        if field:
            body_json.update({
                "field": field
            })
        body = json.dumps(body_json)
        super(BookSearchError, self).__init__(status, body)
        self.content_type = "application/json"

    def __str__(self):
        return str(self.status_code) + " " + self.body


class Error:

    def __init__(self):
        pass

    @classmethod
    def handle_error(cls, response, error):

        logging.error("Type:")
        logging.error(type(error).__name__)
        logging.error("Status:")
        logging.error(error.status)
        logging.error("Message:")
        logging.error(error.message)
        logging.error("Traceback:")
        logging.error(error.traceback)

        if isinstance(error, TemplateError):
            logging.error("Detail:")
            logging.error(error.body)

        if isinstance(error, BookSearchError):
            if error.content_type is not None:
                response.content_type = error.content_type
            return error.body
        else:
            logging.error("Had an unknown error of type %s:\n%s\n%s",
                          error.__class__.__module__ + "." + error.__class__.__name__, error.exception, error.traceback)
            unknown_error = BookSearchError(httplib.INTERNAL_SERVER_ERROR, 0, "An unknown error occurred")
            return cls.handle_error(response, unknown_error)

    @classmethod
    def _raise_error(cls, response, status, code, message, field=None):
        raise BookSearchError(status, code, message, field=field)

    @classmethod
    def raise_not_found(cls, response, message="Not found"):
        logging.error(message)
        cls._raise_error(response, httplib.NOT_FOUND, 1, message)

    @classmethod
    def raise_forbidden(cls, response, message="Forbidden"):
        logging.error(message)
        cls._raise_error(response, httplib.FORBIDDEN, 2, message)

    @classmethod
    def raise_unauthorized(cls, response, message="Unauthorized"):
        logging.error(message)
        cls._raise_error(response, httplib.UNAUTHORIZED, 3, message)

    @classmethod
    def raise_bad_request(cls, response, message="Bad request", field=None):
        logging.error(message)
        cls._raise_error(response, httplib.BAD_REQUEST, 4, message, field=field)

    @classmethod
    def raise_required_field(cls, response, field):
        message = "Missing the required field {0}".format(field)
        logging.error(message)
        cls._raise_error(response, httplib.BAD_REQUEST, 5, message)

    @classmethod
    def raise_user_already_exists(cls, response, field):
        message = "User already exists with email %s" % (field)
        cls._raise_error(response, httplib.BAD_REQUEST, 6, message)

    @classmethod
    def raise_invalid_format(cls, response, field, value, format):
        message = "{0} field has invalid format: {1}. Valid format matches {2}.".format(field, value, format)
        cls._raise_error(response, httplib.BAD_REQUEST, 7, message)

    @classmethod
    def raise_server_error(cls, response, message="Server error"):
        logging.error(message)
        cls._raise_error(response, httplib.INTERNAL_SERVER_ERROR, 8, message)

    @classmethod
    def raise_not_implemented(cls, response, message="Not implemented"):
        logging.error(message)
        cls._raise_error(response, httplib.NOT_FOUND, 9, message)

    @classmethod
    def raise_stripe_error(cls, response, message):
        logging.error(message)
        cls._raise_error(response, httplib.INTERNAL_SERVER_ERROR, 10, message)

    @classmethod
    def raise_user_blocked(cls, response, message="User has been blocked"):
        logging.error(message)
        cls._raise_error(response, httplib.FORBIDDEN, 11, message)


    @classmethod
    def assert_field_required(cls, response, field, value):

        if (isinstance(value, int) or isinstance(value, float)) and value is not None:
            return

        if value is None or len(value) == 0:
            Error.raise_required_field(response, field)
