#!/usr/bin/env python

import os
import yaml

from google.appengine.api import memcache, users


def is_current_user_admin():

	# Check to see if user is logged in with a Google account
	google_user = users.get_current_user()
	if not google_user:
		return False

	# Check to see if user is logged in with a Google account marked as an admin
	if users.is_current_user_admin():
		return True

	# Check to see if user is logged in with a Google account that is on the admin whitelist
	memcache_key = "admin_whitelist"
	admin_whitelist = memcache.get(memcache_key)
	if admin_whitelist is None:
		controller_folder = os.path.dirname(__file__)
		root_folder = os.path.dirname(controller_folder)
		whitelist_yaml_path = os.path.join(root_folder, "resources/admin_whitelist.yaml")
		whitelist_yaml = open(whitelist_yaml_path, "r")
		admin_whitelist_dict = yaml.load(whitelist_yaml)
		admin_whitelist = admin_whitelist_dict.get("whitelist")
		memcache.set(memcache_key, admin_whitelist)

	# Check access
	return google_user.email() in admin_whitelist
