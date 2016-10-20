from functools import wraps

from edgenews.core.user import UserSchema, NewUserSchema

from marshmallow_jsonapi.flask import Schema as JsonAPISchema
from marshmallow_jsonapi import fields
from marshmallow import ValidationError

class SerializeUserSchema(JsonAPISchema, UserSchema):

    id = fields.Str(dump_only=True)

    class Meta:
        type_ = 'user'
        self_view = 'api.user_resource'
        self_view_kwargs = {'name': '<name>'}
        self_view_many = 'api.users_resource'


class SerializeNewUserSchema(JsonAPISchema, NewUserSchema):

    id = fields.Str(dump_only=True)

    class Meta:
        type_ = 'user'


def _fix_string_errors(validation_error_messages):
    """marshmallow_jsonapi doesnt always return a proper jsonapi error object"""

    fixed_errors = []
    for error in validation_error_messages['errors']:

        if isinstance(error, str):
            proper = {'detail': error}

        else:
            proper = error
            
        fixed_errors.append(proper)

    return {'errors': fixed_errors}


def _sort_validation_errors(validation_error_messages):

    def sort_by_pointer(d):
        return d['source']['pointer']

    errors = validation_error_messages['errors']
    sorted_errors = list(sorted(errors, key=sort_by_pointer))
    validation_error_messages['errors'] = sorted_errors

    return validation_error_messages


def error_to_response(validation_error):

    response =_add_error_details(validation_error.messages)

    return response


def _add_error_details(validation_error_messages):

    properly_formed = _fix_string_errors(validation_error_messages)

    for error in properly_formed['errors']:
        error['status'] = '400'
        error['title'] = 'Validation Error'

    sorted_messages = _sort_validation_errors(properly_formed)

    return sorted_messages


def deserialize_user(json_api_request):

    result = SerializeNewUserSchema(strict=True).load(json_api_request)
    return result.data


def _users(user):

    return _serialize(user,
                      id_field='name',
                      fields=['name', 'email'],
                      schema=UserSchema)


_ERROR_MAPPING = {
    'username already taken':
        {'status': '409',
         'title': 'User Already Exists'},
    'email address already in use':
        {'status': '409',
         'title': 'User Already Exists'},
    }

_UNKNOWN_ERROR = {'status': '500',
                  'title': 'An Unknown Error Occurred'}

def _msg(msg):

    error = _ERROR_MAPPING.get(msg, _UNKNOWN_ERROR)
    error['detail'] = msg
    response = {'errors': [error]}

    return response


def users_to_response(user_msg):

    user, msg = user_msg

    if user is not None:
        response = _users(user)

    else:
        response = _msg(msg)

    return response


def _add_id_field(record, id_field):

    record['id'] = record[id_field]

    return record


def _assure_id(fields):

    fields = set(fields)
    fields.add('id')

    return fields


def _serialize(record, id_field, fields, schema):

    if isinstance(record, list):
        many = True
        record_proper = [_add_id_field(r, id_field) for r in record]

    else:
        record_proper = _add_id_field(record, id_field)
        many = False

    fields = _assure_id(fields)

    serialized = SerializeUserSchema(only=fields).dump(record_proper, many=many).data

    return serialized


def _get_status_code(jsonapi_response):

    if 'data' in jsonapi_response:
        status_code = 200

    elif 'errors' in jsonapi_response:
        first_error = jsonapi_response['errors'][0]
        status_code = int(first_error['status'])

    else:
        status_code = 500

    return status_code


def add_status_code(response_func):

    @wraps(response_func)
    def wrapper(*args, **kwargs):
        response = response_func(*args, **kwargs)
        status = _get_status_code(response)
        return response, status

    return wrapper