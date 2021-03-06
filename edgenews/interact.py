# -*- coding: utf-8 -*-
from edgenews import core, store


class UserManager:

    def __init__(self):

        self._repo = store.Registry.get_repo('user')

    def create_user(self, new_user):

        stored = None

        user = core.user.init(new_user)

        exists, exist_msg = self.user_exists(user)
        if exists:
            msg = exist_msg
        else:
            try:
                stored = self._repo.save(user)
                msg = 'ok'
            except Exception as e:
                msg = str(e)

        return stored, msg


    def user_exists(self, user):

        exists = False

        found_by_name, msg = self.get_user(user['name'])
        if found_by_name is not None and msg == 'ok':
            exists = True
            msg = 'username already taken'
        else:
            found_by_email, msg = self.get('email', user['email'])
            if found_by_email is not None and msg == 'ok':
                exists = True
                msg = 'email address already in use'
        return exists, msg


    def get(self, field, value):

        try:
            user = self._repo.first(field, value)
            msg = 'ok'

        except ValueError as e:
            user, msg = None, str(e)

        return user, msg


    def get_user(self, name):

        user, msg = self.get('name', name)

        return user, msg


    def authenticate(self, name, password):

        user, msg = self.get_user(name)
        if msg is 'ok':

            try:
                user = core.user.authenticate(user, password)

            except ValueError as e:
                user = None
                msg = 'could not authenticate'

        return user, msg


    def list_users(self):

        try:
            users = self._repo.all()
            msg = 'ok'

        except Exception as e:
            users = None
            msg = str(e)

        return users, msg
