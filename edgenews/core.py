# -*- coding: utf-8 -*-
import voluptuous as schema
from voluptuous.humanize import humanize_error
from datetime import datetime
import uuid
import hashlib

base_user_schema = {
    schema.Required('name'): schema.All(str, schema.Length(min=1, max=255)),
    schema.Required('email'): schema.All(
        str,
        schema.Length(min=1, max=255),
        schema.Email(schema.All(str, schema.Length(min=1, max=255))))
}
base_user_validator = schema.Schema(base_user_schema)

new_user_schema = {
    schema.Required('plain_password'): schema.All(str, schema.Length(min=1, max=255))
}
new_user_validator = schema.Schema(base_user_schema).extend(new_user_schema)

user_schema = {
    schema.Required('salt'): schema.All(bytes, schema.Length(min=16, max=16)),
    schema.Required('hashed_password'): schema.All(bytes, schema.Length(min=32, max=32)),
    schema.Required('is_active'): bool,
    schema.Required('is_anonymous'): bool,
}
user_validator = schema.Schema(base_user_schema).extend(user_schema)


def _is_valid(record, validator):
    """
    Returns: bool
    """
    try:
        validated = validator(record)
        is_valid = True
    except (schema.Invalid, schema.MultipleInvalid) as e:
        print(e.msg)
        is_valid = False
    return is_valid

def is_valid_new_user(user):
    """
    Returns: bool
    """
    return _is_valid(user, new_user_validator)

def is_valid_user(user):
    return _is_valid(user, user_validator)


def _sha256hash(bytes):
    hasher = hashlib.sha256()
    hasher.update(bytes)
    hashed = hasher.digest()
    return hashed

def _hash_with_salt(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().bytes
    full = password.encode('utf-8') + salt
    hashed = _sha256hash(full)
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
