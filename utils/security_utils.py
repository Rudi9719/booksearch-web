#!/usr/bin/env python

from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha512

# Create crypto context
_crypto_context = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", all__vary_rounds=0.1,
                              pbkdf2_sha256__default_rounds=80000)

def encrypt(password):
    return _crypto_context.encrypt(password)

def verify(password, password_hash):
    return _crypto_context.verify(password, password_hash)
