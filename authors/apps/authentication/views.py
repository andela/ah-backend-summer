from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    TwitterAuthSerializer, GoogleFacebookAuthSerializer
)

import os
import twitter

import facebook

from google.oauth2 import id_token
from google.auth.transport import requests

from .social_login import(login_or_register_social_user)


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get(
            'user', {}) if 'user' in request.data else request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get(
            'user', {}) if 'user' in request.data else request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get(
            'user', {}) if 'user' in request.data else request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TwitterAuthAPIView(GenericAPIView):
    """
    Handle login of a Twitter user via the Twitter Api. 
    The Twitter Api takes parameters of consummer key, consumer secret,
    access token and access token secret. It then verifies the credentials
    and returns the twitter user information

    login_or_register_social_user method, takes in twitter user object and
    verifies if the user is already in the database and returns logged in user
    with a login token if user exists in database. Else, it registers the user
    and logs in the user
    """
    permission_classes = (AllowAny,)
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        """This method returns a logged in Twitter user"""
        access_token = request.data.get('access_token', {})
        access_token_secret = request.data.get('access_token_secret', {})

        serializer = self.serializer_class(data={'access_token': access_token,
                                                 'access_token_secret': access_token_secret
                                                 })
        serializer.is_valid(raise_exception=True)

        # verify and return twitter user information
        twitter_client_key = os.getenv('TWITTER_OAUTH1_KEY')
        twitter_client_secret = os.getenv('TWITTER_OAUTH1_SECRET')

        api = twitter.Api(consumer_key=twitter_client_key,
                          consumer_secret=twitter_client_secret,
                          access_token_key=access_token,
                          access_token_secret=access_token_secret)

        twitter_user = api.VerifyCredentials(include_email="true")
        twitter_user = twitter_user.__dict__

        return login_or_register_social_user(twitter_user)


class GoogleAuthAPIView(GenericAPIView):
    """
    Handle login of a Google user via the Google oauth2. 
    id_token is an open id that allows Clients to verify the identity of the 
    End-User based on the authentication performed by an Authorization Server, 
    as well as to obtain basic profile information about the End-User in an 
    interoperable and REST-like manner.

    login_or_register_social_user method, takes in google user object and
    verifies if the user is already in the database and returns logged in user
    with a login token if user exists in database. Else, it registers the user
    and logs in the user
    """
    permission_classes = (AllowAny,)
    serializer_class = GoogleFacebookAuthSerializer

    def post(self, request):
        """This method returns a logged in Google user"""
        access_token = request.data.get('access_token', {})

        serializer = self.serializer_class(data={'access_token': access_token})
        serializer.is_valid(raise_exception=True)

        # verify and return google user information
        google_user = id_token.verify_oauth2_token(
            access_token, requests.Request())

        return login_or_register_social_user(google_user)


class FacebookAuthAPIView(GenericAPIView):
    """
    Handle login of a Facebook user via the Facebook Graph API. 
    The Graph API returns a graph object that contains user information

    login_or_register_social_user method, takes in Facebook user object and
    verifies if the user is already in the database and returns logged in user
    with a login token if user exists in database. Else, it registers the user
    and logs in the user
    """
    permission_classes = (AllowAny,)
    serializer_class = GoogleFacebookAuthSerializer

    def post(self, request):
        """This method returns a logged in Facebook user"""
        access_token = request.data.get('access_token', {})

        serializer = self.serializer_class(data={'access_token': access_token})
        serializer.is_valid(raise_exception=True)

        # verify and return facebook user information
        graph = facebook.GraphAPI(access_token=access_token)
        facebook_user = graph.get_object(id='me', fields='email, name')

        return login_or_register_social_user(facebook_user)
