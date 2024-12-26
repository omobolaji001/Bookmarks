#!/usr/bin/env python3
""" Contains email authentication backend file """
from django.contrib.auth.models import User
from .models import Profile


class EmailAuthBackend:
    """ Authentication using an e-mail address """

    def authenticate(self, request, username=None, password=None):
        """ Authenticates current user """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """ Retrieves the user object for the duration of the session """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def create_profile(backend, user, *args, **kwargs):
        """ Creates profile for social authentication """
        Profile.objects.get_or_create(user=user)
