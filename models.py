#!/usr/bin/env python

import datetime
import json
import logging
import random

from dateutil.relativedelta import relativedelta
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext.db import NotSavedError
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

import constants
from utils import security_utils


class BaseModel(ndb.Model):

    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def __repr__(self):
        return json.dumps(self.to_external_dict())

    @property
    def external_key(self):
        key = None
        try:
            key = self.key
        except NotSavedError:
            pass

        if key is None:
            return None

        return key.urlsafe()

    @classmethod
    def fetch_all(cls):
        return cls.query().fetch()

    @classmethod
    def fetch_all_in_order(cls, order):
        return cls.query().order(order).fetch()

    @classmethod
    def count_all(cls):
        return cls.query().count(keys_only=True)

    @classmethod
    def delete_all(cls):
        keys = []
        for entity in cls.query().fetch():
            keys.append(entity.key)
        if len(keys) > 0:
            ndb.delete_multi(keys)

    @classmethod
    def get_by_external_key(cls, external_key):
        key = cls.key_from_external_key(external_key)
        if not key:
            return None
        return key.get()

    @classmethod
    def get_by_external_keys(cls, external_keys):

        # Get all the keys
        keys = []
        for external_key in external_keys:
            key = cls.key_from_external_key(external_key)
            if key:
                keys.append(key)

        # Return entities
        return filter(None, ndb.get_multi(keys))

    @classmethod
    def get_by_keys(cls, keys):
        return filter(None, ndb.get_multi(keys))

    @classmethod
    def delete_by_external_key(cls, external_key):
        return cls.key_from_external_key(external_key).delete()

    @classmethod
    def key_from_external_key(cls, external_key):
        key = None
        try:
            key = ndb.Key(urlsafe=external_key)
            if key and key.kind() != cls.__name__:
                key = None
        except ProtocolBufferDecodeError as e:
            logging.exception(
                "An error occurred attempting to get key from external key: {0}. {1}".format(external_key, e.message))
        except TypeError as e:
            logging.exception(
                "An error occurred attempting to get key from external key: {0}. {1}".format(external_key, e.message))
        return key

    def to_external_dict(self):
        return {
            "id": self.external_key,
            "created": self.created.isoformat() if self.created else None,
            "modified": self.modified.isoformat() if self.modified else None
        }


class PhotoSize(ndb.Model):

    content_length = ndb.IntegerProperty()
    height = ndb.IntegerProperty()
    path = ndb.StringProperty()
    width = ndb.IntegerProperty()

    def to_external_dict(self):
        return {
            "content_length": self.content_length,
            "height": self.height,
            "width": self.width
        }


class Photo(BaseModel):

    content_type = ndb.StringProperty()
    original_size = ndb.StructuredProperty(PhotoSize)
    large_size = ndb.StructuredProperty(PhotoSize)
    medium_size = ndb.StructuredProperty(PhotoSize)
    small_size = ndb.StructuredProperty(PhotoSize)

    def to_external_dict(self):
        ext_dict = super(Photo, self).to_external_dict()

        ext_dict.update({
            "content_type": self.content_type,
            "sizes": {
                "large": self.large_size.to_external_dict(),
                "medium": self.medium_size.to_external_dict(),
                "small": self.small_size.to_external_dict()
            }
        })
        return ext_dict

class Book(BaseModel):
    
    subject = ndb.StringProperty()
    isbn = ndb.StringProperty(required=True)
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    icon = ndb.StringProperty()
    price = ndb.StringProperty()
    owner = ndb.StringProperty(required=True)

    @classmethod
    def get_by_subject(cls, subject):
        return cls.query(cls.subject == subject.lower()).fetch()
    
    @classmethod
    def get_by_isbn(cls, isbn):
        return cls.query(cls.isbn == isbn.lower()).fetch()

    @classmethod
    def get_by_title(cls, title):
        return cls.query(cls.title == title.lower()).fetch()

    @classmethod
    def get_by_author(cls, author):
        return cls.query(cls.author == author.lower()).fetch()

    @classmethod
    def get_by_owner(cls, owner):
        return cls.query(cls.owner == owner.lower()).fetch()

    def to_external_dict(self):
        return {
            "subject": self.subject,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "icon": self.icon,
            "price": self.price,
            "owner": self.owner
        }





class Item(BaseModel):
    type = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    image = ndb.StringProperty()
    owner = ndb.StringProperty(required=True)
    price = ndb.StringProperty()
    
    @classmethod
    def get_by_type(cls, type):
        return cls.query(cls.type == type.lower()).fetch()
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name == name.lower()).fetch()
    
    @classmethod
    def get_by_owner(cls, owner):
        return cls.query(cls.owner == title.owner()).fetch()

    def to_external_dict(self):
        ext_dict = super(Item, self).to_external_dict()
        ext_dict.update({
                        "type": self.type,
                        "name": self.name,
                        "image": self.image,
                        "owner": self.owner,
                        "price": self.price
                        })
        return ext_dict




class User(BaseModel):

    email = ndb.StringProperty()
    has_logged_in = ndb.BooleanProperty()
    login_type = ndb.StringProperty(default="email")
    password_hash = ndb.StringProperty(indexed=False)
    reset_token = ndb.StringProperty()
    reset_token_expiration = ndb.DateTimeProperty()
    username = ndb.StringProperty()
    u_number = ndb.StringProperty(required=True)
    name = ndb.StringProperty()

    def _pre_put_hook(self):
        if self.email is not None:
            self.email = self.email.lower()
        self.username = self.username.lower()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.password_hash = security_utils.encrypt(password)

    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email.lower()).get()

    @classmethod
    def get_by_email_and_password(cls, email, password):
        user = cls.get_by_email(email)
        if user:
            if security_utils.verify(password, user.password_hash):
                return user
        return None
    
    @classmethod
    def get_by_username_and_password(cls, username, password):
        user = cls.get_by_username(username)
        if user:
            if security_utils.verify(password, user.password_hash):
                return user
        return None


    @classmethod
    def get_by_reset_token(cls, reset_token):
        return cls.query(cls.reset_token == reset_token).get()

    @classmethod
    def get_by_username(cls, username):
        return cls.query(cls.username == username.lower()).get()
    
    @classmethod
    def get_by_u_number(cls, u_number):
        return cls.query(cls.u_number == u_number.lower()).get()

    def to_external_dict(self):
        ext_dict = super(User, self).to_external_dict()
        ext_dict.update({
            "email": self.email,
            "username": self.username,
            "u_number": self.u_number
        })
        return ext_dict

    def to_auth_dict(self):
        auth_dict = self.to_external_dict()
        auth_dict.update({
            "email": self.email,
            })
        return auth_dict


class BaseUserModel(BaseModel):

    user_key = ndb.KeyProperty(kind=User, required=True)

    @property
    def user(self):
        return self.user_key.get()

    @classmethod
    def get_by_user_key(cls, user_key):
        return cls.query(cls.user_key == user_key).get()

    @classmethod
    def get_most_recent_by_user_key(cls, user_key):
        return cls.query(cls.user_key == user_key).order(-cls.created).get()

    @classmethod
    def fetch_by_user_key(cls, user_key, order=None, page=None, page_size=constants.PAGE_SIZE, keys_only=False):

        results = None

        query = cls.query(cls.user_key == user_key)
        if order:
            query = query.order(order)
        if page:
            results = query.fetch(offset=(page - 1) * page_size, limit=page_size, keys_only=keys_only)
        else:
            results = query.fetch(keys_only=keys_only)

        return results


class Token(BaseUserModel):

    expiration = ndb.DateTimeProperty()

    def _pre_put_hook(self):
        if not self.key.id():
            self.expiration = datetime.datetime.now() + datetime.timedelta(days=30)

    def is_valid(self):
        return datetime.datetime.now() < self.expiration

    def to_external_dict(self):
        ext_dict = super(Token, self).to_external_dict()
        ext_dict.update({
            "expiration": self.expiration.isoformat()
        })
        return ext_dict


class BaseProfile(BaseUserModel):

    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    u_number = ndb.StringProperty(required=True)
    
    @property
    def abbreviated_name(self):
        return "{0} {1}.".format(self.first_name, self.last_name[0])

    def to_external_dict(self):
        ext_dict = super(BaseProfile, self).to_external_dict()
        ext_dict.update({
            "abbreviated_name": self.abbreviated_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "u_number": self.u_number
        })
        return ext_dict

    def to_auth_dict(self):
        auth_dict = self.to_external_dict()
        auth_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
        })
        return auth_dict


class GeneralShardedCounterConfig(ndb.Model):

    SHARD_KEY_TEMPLATE = 'counter-{0}-{1}'

    num_shards = ndb.IntegerProperty(default=10)

    @classmethod
    def all_keys(cls, name, num_shards=None):

        # Get config
        config = cls.get_or_insert(name)

        # Get shard keys
        shard_keys = list()
        for index in range(num_shards if num_shards else config.num_shards):
            shard_key_string = GeneralShardedCounterConfig.SHARD_KEY_TEMPLATE.format(name, index)
            shard_keys.append(ndb.Key(GeneralShardedCounter, shard_key_string))

        return shard_keys


class GeneralShardedCounter(BaseModel):

    count = ndb.IntegerProperty(default=0)

    @classmethod
    def get_count(cls, name, num_shards=None):

        # Look in cache
        total = memcache.get(name)
        if total is not None:
            return total

        # Add shards
        total = 0
        all_keys = GeneralShardedCounterConfig.all_keys(name, num_shards=num_shards)
        for counter in ndb.get_multi(all_keys):
            if counter is not None:
                total += counter.count

        # Store value in memcache
        memcache.set(name, total)

        return total

    @classmethod
    @ndb.transactional(retries=5)
    def increase_shards(cls, name, num_shards):

        # Get config
        config = GeneralShardedCounterConfig.get_or_insert(name)

        # Increase shard count
        if config.num_shards < num_shards:
            config.num_shards = num_shards
            config.put()

    @classmethod
    def increment(cls, name, delta=1):

        # Get config
        config = GeneralShardedCounterConfig.get_or_insert(name)

        # Increment
        cls._increment(name, delta, config.num_shards)

    @classmethod
    @ndb.transactional()
    def _increment(cls, name, delta, num_shards):

        # Choose random index
        index = random.randint(0, num_shards - 1)

        # Get counter
        shard_key_string = GeneralShardedCounterConfig.SHARD_KEY_TEMPLATE.format(name, index)
        counter = cls.get_by_id(shard_key_string)
        if counter is None:
            counter = cls(id=shard_key_string)

        # Increment
        counter.count += delta
        counter.put()

        # Update memcache
        if delta > 0:
            memcache.incr(name, delta)
        else:
            memcache.decr(name, -delta)

    @classmethod
    def reset_count(self, name, num_shards=None):

        # Delete for all keys
        all_keys = GeneralShardedCounterConfig.all_keys(name, num_shards=num_shards)
        ndb.delete_multi(all_keys)

        # Clear memcache
        memcache.delete(name)



class Device(BaseUserModel):

    device_token = ndb.StringProperty()

    @classmethod
    def get_by_user_key_and_device_token(cls, user_key, device_token):
        return cls.query(cls.user_key == user_key, cls.device_token == device_token).get()

    def to_external_dict(self):
        ext_dict = super(Device, self).to_external_dict()
        ext_dict.update({
            "device_token": self.device_token
        })
        return ext_dict



class BlockedUser(BaseUserModel):

    blocked_user_key = ndb.KeyProperty(kind=User)

    @property
    def blocked_user(self):
        return self.blocked_user_key.get()

    @classmethod
    def fetch_by_blocked_user_key(cls, blocked_user_key):
        return cls.query(cls.blocked_user_key == blocked_user_key).fetch()

    @classmethod
    def get_by_user_key_and_blocked_user_key(cls, user_key, blocked_user_key):
        return cls.query(cls.user_key == user_key, cls.blocked_user_key == blocked_user_key).get()

    @classmethod
    def is_user_key_blocked_by_user_key(cls, blocked_user_key, user_key):
        return cls.get_by_user_key_and_blocked_user_key(user_key, blocked_user_key) is not None


class ReportedUser(BaseUserModel):

    explanation = ndb.StringProperty()
    reported_by_user_key = ndb.KeyProperty(kind=User)


