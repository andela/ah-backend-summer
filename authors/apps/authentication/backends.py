import json
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from rest_framework.response import Response

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    This is a custom class and it handles the authentication of a
    token provided a user
    It overwrites the BaseAuthentication class provided by the restframework
    """
    token_header_prefix = 'Bearer'

    def authenticate(self, request):
        """This method will authenticate a user on provision of
        a valid Bearer token
        It collects the token from the request headers on ever
        request performed
        It checks whether the provided token is a Bearer token
        It also checks whether a token is provided.
        Then is passes the token down to another method to validate it.
        """
        request.user = None
        authentication_header = authentication.get_authorization_header(
            request).split()

        if not authentication_header:
            # Returns none if there is no authentication header provided
            return None
        if len(authentication_header) == 1:
            # Raise an error if the authentication header has only a token or
            # Bearer
            msg = 'You should provide both the Bearer prefix and the token'
            raise exceptions.AuthenticationFailed(msg)
        if len(authentication_header) > 2:
            # Raise an error if the authentication has more than a token and
            # Bearer
            msg = 'sorry you have provided a long token'
            raise exceptions.AuthenticationFailed(msg)

        # The authentication header is list which is split into a prefix and
            # token
        prefix = authentication_header[0].decode('utf-8')
        token = authentication_header[1].decode('utf-8')

        # If the provided Bearer prefix is not equal to Bearer, raise an
        # exception
        if prefix.lower() != self.token_header_prefix.lower():
            msg = 'wrong prefix, please use Bearer'
            raise exceptions.AuthenticationFailed(msg)

        return self.validate_credentials(request, token)

    def validate_credentials(self, request, token):
        """The validate_credentials method decods to validate
        the sent in user token
        It receives two variables a request and a token
        It will first try to decode the token and generate a user payload
        If this fails it will raise an exception which might include
        """

        try:
            user_payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignature:
            msg = ('Token has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            msg = (
                'Error decoding signature. \
Please check the token you have provided.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=user_payload['id'])
            if user.is_active:
                return (user, token)
        except User.DoesNotExist:
            msg = 'A user matching this token was not found.'
            raise exceptions.AuthenticationFailed(msg)
