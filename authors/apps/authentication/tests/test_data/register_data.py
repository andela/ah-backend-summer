"""Test data registration"""
valid_register_data = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'ia83naJS'
    }
}

register_short_password = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'gsh'
    }
}

register_invalid_password = {
    'user': {
        'email': 'abc@abc.com',
        'username': 'abc123',
        'password': 'gsh/sd]sd'
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
        'password': 'ia83naJS'
    }
}

expired_link = '/api/v1/users/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTgsImV4cCI6MTU0OTIwMTQ3OX0.2kZDXpwA8SKbcakzhofPC0nYLagSd1ISp9JNWo5C3as/'
invalid_link = '/api/v1/users/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ8.eyJpZCI6NTgsImV4cCI6MTU0OTIwMTQ3OX0.2kZDXpwA8SKbcakzhofPC0nYLagSd1ISp9JNWo5C3as/'
