# -*- coding: utf-8 -*-
import voluptuous as schema
from voluptuous.humanize import humanize_error
from marshmallow import Schema, fields, validate
from datetime import datetime
import uuid
import hashlib


class BaseUserSchema(Schema):
    name = fields.String(required=True,
                         validate=[validate.Length(min=1, max=255)])
    email = fields.Email(required=True,
                         validate=[validate.Length(min=1, max=255)])

class NewUserSchema(BaseUserSchema):
    plain_password = fields.String(required=True,
                                   validate=[validate.Length(min=1, max=255)])

class UserSchema(BaseUserSchema):
    salt = fields.String(required=True)
    hashed_password = fields.String(required=True)
    is_active = fields.Bool(required=True)


def _is_valid(record, validator):
    """
    Returns: bool
    """
    data, errors = validator(record)
    is_valid = (errors == {})
    return is_valid

def is_valid_new_user(user):
    """
    Returns: bool
    """
    return _is_valid(user, NewUserSchema().load)

def is_valid_user(user):
    return _is_valid(user, UserSchema().load)


def _sha256hash(string):
    hasher = hashlib.sha256()
    hasher.update(string.encode('utf-8'))
    hashed = hasher.digest().hex()
    return hashed

def _hash_with_salt(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().hex
    full = password + salt
    print('############')
    print(full)
    hashed = _sha256hash(full)
    print(hashed)
    return hashed, salt

def prepare_user(new_user):
    user = dict(new_user)
    plain_password = user.pop('plain_password')
    user['hashed_password'], user['salt'] = _hash_with_salt(plain_password)
    user['is_active'] = True
    user['is_anonymous'] = False
    return user

def authenticate_user(user, password):
    hashed, _ = _hash_with_salt(password, user['salt'])
    if hashed == user['hashed_password']:
        user['is_authenticated'] = True
        return user
    raise ValueError("Password doesnt match")
