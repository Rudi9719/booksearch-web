#!/usr/bin/env python

import datetime
import re
import uuid

import constants
import models
from api.base import BaseApi, authorize
from api.error import Error
from frameworks.bottle import request, response
from utils import request_utils, validation_utils


class UserApi(BaseApi):

    def __init__(self):
        BaseApi.__init__(self)
    
    def _uname_login(self, username, password):

        # Verify param
        if not username or not password:
            Error.raise_bad_request(response)

        # Attempt login
        user = models.User.get_by_username_and_password(username, password)

        return user

    def _generate_token_for_user_key(self, user_key, delete_existing_tokens=False):

        # Delete existing token
        if delete_existing_tokens:
            tokens = models.Token.fetch_by_user_key(user_key)
            for token in tokens:
                token.key.delete()

        # Create new token
        token = models.Token()
        token.user_key = user_key
        token.put()

        return token

    def check_availability(self, uname):

        # Get param
        username = uname

        # Validate format
        if not re.match(validation_utils.REGEX_USERNAME, username):
            Error.raise_invalid_format(response, "username", username, validation_utils.REGEX_USERNAME)

        # Lookup username
        user = models.User.get_by_username(username)

        return {
            "available": (user is None)
        }

    def create(self, unum):
        user = models.User()
        user.username = request.json.get("uname")
        user.email = request.json.get("email")
        user.u_number = unum
        user.name = request.json.get("name")
        user.password = request.json.get("upass")
        user.put()
        return dict(code=200, message="Successfully created user by unumber " + unum + ".", valid=True)
    
    
    def login(self):

        # Get login type
        username = request.json.get("uname")
        password = request.json.get("upass")

        return self.login_internal(username, password)

    def login_internal(self, username, password):
        delete_existing_tokens = False
        # Attempt login
        user = None
        user = self._uname_login(username, password)

        # Validate user
        if not user:
            Error.raise_unauthorized(response)

        # Generate token
        token = self._generate_token_for_user_key(user.key, delete_existing_tokens=delete_existing_tokens)

        # Mark user as logged in
        if not user.has_logged_in:
            user.has_logged_in = True
            user.put()

        return dict(code=200, access_token=token.external_key, valid=True)

    @authorize(error_silently=True)
    def logout(self, logged_in_user=None):
        return self.logout_internal(logged_in_user)

    def logout_internal(self, logged_in_user):

        # Delete token
        if logged_in_user:
            tokens = models.Token.fetch_by_user_key(logged_in_user.key)
            for token in tokens:
                token.key.delete()

    def forgot_password(self):

        # Get params
        email = request.json.get("email")

        return self.forgot_password_internal(email)

    def forgot_password_internal(self, email, send_email=True):

        # Verify params
        Error.assert_field_required(response, "email", email)

        # Lookup user by email
        user = models.User.get_by_email(email)
        if user and user.login_type == constants.USER_LOGIN_TYPE_EMAIL:
            # Add reset token
            user.reset_token = str(uuid.uuid4())
            user.reset_token_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
            user.put()

            # Send email
            if send_email:
                self.email_api.send_forgot_password_email(user)

        return {

        }

    def reset_password(self):

        # Get params
        password = request.json.get("password")
        reset_token = request.json.get("reset_token")

        # Verify params
        Error.assert_field_required(response, "password", password)
        Error.assert_field_required(response, "reset_token", reset_token)

        # Get user
        user = models.User.get_by_reset_token(reset_token)
        if not user:
            Error.raise_bad_request(response)

        # Check reset token expiration
        reset_token_expired = user.reset_token_expiration < datetime.datetime.now()
        if reset_token_expired:
            Error.raise_bad_request(response)

        # Update password
        user.password = password
        user.reset_token = None
        user.reset_token_expiration = None
        user.put()

        # Send email
        self.email_api.send_reset_password_email(user)

        # Log user in
        return self.login_internal(constants.USER_LOGIN_TYPE_EMAIL, user.email, password, None)

    @authorize()
    def change_password(self, logged_in_user=None):
        return self.change_password_internal(logged_in_user)

    def change_password_internal(self, logged_in_user):

        # Enforce login type
        if logged_in_user.login_type != constants.USER_LOGIN_TYPE_EMAIL:
            Error.raise_forbidden(response, "Cannot change password for user that doesn't login with email")

        # Get params
        current_password = request_utils.get_value("current_password", request.json)
        new_password = request_utils.get_value("new_password", request.json)

        # Verify current password matches
        user = models.User.get_by_email_and_password(logged_in_user.email, current_password)
        if not user:
            Error.raise_bad_request(response, "Current password is incorrect")

        # Update password
        logged_in_user.password = new_password
        logged_in_user.put()

        # Send email
        self.email_api.send_reset_password_email(user)

    def whoami(self):
        token = request.headers.get("authorization_token")
        user = models.Token.get_by_user_key(token)
        uname = user.username
        return dict(code=200, message="Successfully authenticated " + uname + ".", valid=True)

