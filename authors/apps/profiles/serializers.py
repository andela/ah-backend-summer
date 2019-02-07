from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("username", "first_name", "last_name", "bio", "image", )

    def validate(self, data):
        """
        validate method checks if user passes data with non profile fields then
        returns an error otherwise returns validated data
        """
        serializer_fields = [field for field in self.fields]
        unknown_fields = set(self.initial_data.keys()) - \
            set(self.fields.keys())
        eror_message = "Please only provide the profile fields"
        if unknown_fields:
            raise serializers.ValidationError(eror_message)
        return data
