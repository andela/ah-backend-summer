from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.reverse import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default="author.jpg", upload_to="profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    follows = models.ManyToManyField('self', related_name='followed_by',
                                     symmetrical=False)

    def follow(self, profile):
        # Follow if we are not already following
        self.follows.add(profile)

    def unfollow(self, profile):
        # Unfollow if we are already following.
        self.follows.remove(profile)

    def is_following(self, profile):
        # True if we are following, False otherwise.
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        # True if profile follows us, False otherwise.
        return self.followed_by.filter(pk=profile.pk).exists()

    @property
    def url(self):
        return settings.URL + reverse('profiles:profile-detail-update',
                                      kwargs={"username": self.username})

    def __str__(self):
        return self.username


def user_post_save_reciever(*args, **kwargs):
    # Creates a profile after user has been registered
    created = kwargs.get("created")
    user = kwargs.get("instance")
    if created:
        Profile.objects.get_or_create(user=user,
                                      username=user.username)


post_save.connect(user_post_save_reciever, sender=settings.AUTH_USER_MODEL)
