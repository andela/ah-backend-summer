"""Test data"""
valid_register_data = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'ia83na.JS'
    }
}

valid_register_data_2 = {
    'user': {
        'email': 'admin@email.com',
        'username': 'admin',
        'password': 'pass1234'
    }
}

valid_login_data = {
    'user': {
        'email': 'abc@abc.com',
        'password': 'ia83na.JS'
    }
}

valid_login_data_2 = {
    'user': {
        'email': 'admin@email.com',
        'password': 'pass1234'
    }
}

register_short_password = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'gsh'
    }
}

register_no_email = {
    'user': {
        'username': 'abc123',
        'password': 'gsh'
    }
}

register_no_username = {
    'user': {
        'email': 'abc@abc.com',
        'password': 'gsh'
    }
}

register_no_username_password_email = {
    'user': {
    }
}

register_no_password = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123'
    }
}

register_invalid_email = {
    'user': {
        'email': 'abc.com',
        'username': 'abc123',
        'password': 'ia83na.JS'
    }
}

login_no_email = {
    'user': {
        'password': 'pass1234'
    }
}

login_no_password = {
    'user': {
        'email': 'admin@email.com'
    }
}

login_invalid_email = {
    'user': {
        'email': 'admin@.com',
        'password': 'pass1234'
    }
}

login_unregistered_email = {
    'user': {
        'email': 'admin1234@email.com',
        'password': 'pass1234'
    }
}

login_invalid_password = {
    'user': {
        'email': 'admin@email.com',
        'password': 'pass1234fwfw'
    }
}

login_no_email_password = {
    'user': {}
}
