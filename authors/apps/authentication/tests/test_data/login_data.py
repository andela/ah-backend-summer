"""Test data login"""

valid_login_data = {
    'user': {
        'email': 'abc@abc.com',
        'password': 'ia83naJS'
    }
}

login_no_email = {
    'user': {
        'password': 'ia83naJS'
    }
}

login_no_password = {
    'user': {
        'email': 'abc@abc.com'
    }
}

login_invalid_email = {
    'user': {
        'email': 'abc.com',
        'password': 'ia83naoJS'
    }
}

login_unregistered_email = {
    'user': {
        'email': 'abcjajs@abc.com',
        'password': 'ia83naJS'
    }
}

login_invalid_password = {
    'user': {
        'email': 'abc@abc.com',
        'password': 'ia83na'
    }
}

login_no_email_password = {
    'user': {}
}
valid_token_unexisting_user = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
MSwiZXhwIjozMDMyMDE1NjUxNH0.z2yxT0WvOuE2AXvYIc6LwxoVadV8izp7zFIVf0jsmhY"
expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTQ\
4OTU2MzY5fQ.Eu-0EFROqMrPcWEkcgRJYG0zzK_-IuhODAe8v69rd5o'
