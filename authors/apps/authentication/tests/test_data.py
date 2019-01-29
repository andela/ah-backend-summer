"""Test data"""
valid_register_data = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'ia83na.JS'
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
