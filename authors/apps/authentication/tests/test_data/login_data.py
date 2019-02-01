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
