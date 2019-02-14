from .models import User
from rest_framework.response import Response
from rest_framework import status


def login_or_register_social_user(social_user):
    """
    login_or_register_social_user method, takes in twitter or facebook or
    google user object and verifies if the user is already in the database and
    returns logged in user with a login token if user exists in database.
    Else, it registers the user and logs in the user
    """
    # find user in database
    try:
        user = User.objects.get(email=social_user.get('email'))
    except User.DoesNotExist:
        new_password = User.objects.make_random_password()
        new_social_user = {
            'email': social_user.get('email'),
            'username': social_user.get('name'),
            'password': new_password
        }
        user = User.objects.create_user(**new_social_user)

    return Response({'user': {
        'email': social_user.get('email'),
        'username': social_user.get('name'),
        'token': user.token_generator()
    }
    }, status=status.HTTP_200_OK)
