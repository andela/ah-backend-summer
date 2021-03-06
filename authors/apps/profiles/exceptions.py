from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = {
        'error': 'The Requested profile does not exist.',
        'status': 400
    }
