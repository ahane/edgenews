from edgenews.core.user import UserSchema

from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields


class SerializeUserSchema(Schema, UserSchema):
    id = fields.Str()
    class Meta:
        type_ = 'users'
        self_view = 'api.user_resource'
        self_view_kwargs = {'name': '<name>'}
        self_view_many = 'api.users_resource'

#TODO
# potentially add a User<-Bunch type to do deserialization based on pattern matching
# add errorhandling

def users(record_msg):
    record, msg = record_msg
    if isinstance(record, list):
        many = True
    else:
        record['id'] = record['name']
        many = False
    fields = ('id', 'name', 'email')
    serialized = SerializeUserSchema(only=fields).dump(record, many=many).data
    return serialized