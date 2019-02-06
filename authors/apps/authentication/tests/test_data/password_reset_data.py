"""Test data for password reset feature"""
import jwt
from django.conf import settings

from .login_data import valid_login_data

registered_email = {
    "user": {
        "email": valid_login_data["user"]["email"]
    }  
}

unregistered_email = {
    "user": {
        "email": "jklm@mno.org"
    }
}

new_valid_password = {
    "user": {
        "new_password": "xml123XML"
    }    
}

new_short_password = {
    "user": {
        "new_password": "ab2"
    }    
}

new_invalid_password = {
    "user": {
        "new_password": "abcd@efgh"
    }    
}

new_blank_password = {
    "user": {
        "new_passord":""
    } 
}

token = jwt.encode({
            "email":valid_login_data["user"]["email"],
        },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
reset_link = '/api/v1/user/reset-password/'+ token.decode('utf-8') + '/'

invalid_reset_link = '/api/v1/user/reset-password/'+ token.decode('utf-8') + 'wrongL!NK/'
