from django.db import models
from django.db.models.signals import pre_save

from ..profiles import models as ProfileModel
from .utils import utils


class Article(models.Model):
    """The Article class model defines the Article table model in the DB
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    favoritesCount = models.IntegerField(default=0)
    favorited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    image = models.ImageField(
        upload_to='assets/articles/images',
        blank=True)
    author = models.ForeignKey(ProfileModel.Profile,
                               on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        """Meta class difines extra functions to be ran on the DB
        'ordering = -created_at' ensures that the ordering of articles
        should in a descending order.
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.title


def article_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{utils.create_slug(instance)}-\
            {utils.unique_random_string()}'


pre_save.connect(article_pre_save_receiver, sender=Article)
