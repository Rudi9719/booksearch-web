#!/usr/bin/env python

import re

REGEX_URL = "^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$"
REGEX_USERNAME = "^[a-zA-Z0-9_]+$"
REGEX_CASTING_ID = "^[a-zA-Z0-9_]+$"

def is_url_valid(url):
    return re.match(REGEX_URL, url, re.IGNORECASE)

def is_username_valid(username):
    return re.match(REGEX_USERNAME, username, re.IGNORECASE)

def is_casting_id_valid(casting_id):
    return re.match(REGEX_CASTING_ID, casting_id, re.IGNORECASE)
