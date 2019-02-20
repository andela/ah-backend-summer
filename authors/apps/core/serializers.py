from rest_framework import serializers
from rest_framework import exceptions as rest_framework_exceptions
from . import exceptions as custom_exceptions


class ModelSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False, message=None):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except rest_framework_exceptions.ValidationError as e:
            if not message:
                raise e
            raise custom_exceptions.CustomValidationError(e, message)
