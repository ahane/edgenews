# -*- coding: utf-8 -*-
import uuid
import hashlib

from marshmallow import Schema, fields, validate


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


def _is_valid(record, schema):

    data, errors = schema().load(record)
    is_valid = (errors == {})
    return is_valid


def is_valid_new_user(user):

    return _is_valid(user, NewUserSchema)


def is_valid(user):

    return _is_valid(user, UserSchema)


def _sha256hash(string):

    hasher = hashlib.sha256()
    hasher.update(string.encode('utf-8'))
    hashed = hasher.digest().hex()

    return hashed


def _hash_with_salt(password, salt=None):

    if salt is None:
        salt = uuid.uuid4().hex

    full = password + salt
    hashed = _sha256hash(full)

    return hashed, salt


def init(new_user):

    user = dict(new_user)
    plain_password = user.pop('plain_password')
    user['hashed_password'], user['salt'] = _hash_with_salt(plain_password)
    user['is_active'] = True
    user['is_anonymous'] = False

    return user


def authenticate(user, password):

    hashed, _ = _hash_with_salt(password, user['salt'])

    if hashed == user['hashed_password']:
        user['is_authenticated'] = True
        return user

    else:
        raise ValueError("Password doesnt match")
