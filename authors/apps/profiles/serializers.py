from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "first_name", "last_name", "bio", "image",
                  "following",)

    def get_following(self, instance):
        """
        Method to check whether logged in user is following returned
        profile
        """
        request = self.context.get('request', None)
        if request is None:
            return False
        follower = request.user.profile
        followee = instance
        return follower.is_following(followee)

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
