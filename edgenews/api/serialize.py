from edgenews.core.user import BaseUserSchema

from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields


class SerializeUserSchema(Schema, BaseUserSchema):
    id = fields.Str()
    class Meta:
        type_ = 'users'
        self_view = 'api.user_resource'
        self_view_kwargs = {'name': '<name>'}


def users(record_msg):
    record, msg = record_msg
    record['id'] = record['name']
    serialized = SerializeUserSchema().dump(record).data
    return serialized