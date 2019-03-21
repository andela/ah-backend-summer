from rest_framework import serializers
from .models import Profile
from authors.apps.articles.models import Article


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_of_following = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = ("username", "first_name", "last_name", "bio", "image",
                  "following", "date_of_birth", "followers", "followings", 
                  "number_of_followers", "number_of_following")

    def get_following(self, instance):
        """
        Method to check whether logged in user is following returned
        profile
        """
        request = self.context.get('request', None)
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        follower = request.user.profile
        followee = instance
        return follower.is_following(followee)

    def get_followers(self, instance):
        queryset = instance.followed_by.all()
        followers = [follower.username for follower in queryset]
        return followers

    def get_followings(self, instance):
        queryset = instance.follows.all()
        followings = [following.username for following in queryset]
        return followings

    def get_number_of_following(self, instance):
        return len(instance.follows.all())

    def get_number_of_followers(self, instance):
        return len(instance.followed_by.all())

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
