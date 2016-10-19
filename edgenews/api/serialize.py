from functools import wraps
from edgenews.core.user import BaseUserSchema
#from .resources import api_object


def as_jsonapi_and_statuscode(id_field, type_, fields):

    def as_jsonapi_decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            record, msg = func(*args, **kwargs)

            is_empty = (record == [])
            if not is_empty:

                attributes = {}
                for field in fields:
                    attributes[field] = record[field]

                result = {'data':
                          {'id': record[id_field],
                           'type': type_,
                           'attributes': attributes}}
            else:
                result = {'data': []}

            return result

        return wrapper

    return as_jsonapi_decorator