#!/usr/bin/env python

import models

from api.error import Error
from frameworks.bottle import request, response
from utils import admin_utils


class BaseApi:
    
    def __init__(self):
        pass
    
    def get_user_by_username(self, username):
        
        # Get user
        user = models.User.get_by_username(username)
        if not user:
            Error.raise_not_found(response)
        
        return user
    
    def is_user_blocked_by_user(self, blocked_user, user):
        if blocked_user:
            return models.BlockedUser.is_user_key_blocked_by_user_key(blocked_user.key, user.key)
        else:
            return False

def authorize(error_silently=False, enforced_type=None):
    def decorator(function):
        def inner_decorator(*args, **kwargs):
            
            # Get logged in user
            logged_in_user = None
            token_id = request.get_header("Authorization")
            if token_id:
                token = models.Token.get_by_external_key(token_id)
                if token and token.is_valid():
                    logged_in_user = token.user
        
            # Check user is logged in
            if logged_in_user:
                if enforced_type and logged_in_user.user_type != enforced_type and not error_silently:
                    Error.raise_forbidden(response, "User of type {0} forbidden from accessing this method".format(logged_in_user.user_type))
            else:
                if not error_silently:
                    Error.raise_unauthorized(response)
            
            # Set logged in user
            kwargs["logged_in_user"] = logged_in_user
            
            return function(*args, **kwargs)
        
        return inner_decorator
    return decorator

def require_admin(function):
    
    def decorator(*args, **kwargs):
        
        if not admin_utils.is_current_user_admin():
            Error.raise_forbidden(response)
        
        # Run function
        return function(*args, **kwargs)
    
    return decorator
