from django.conf import settings
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
    # users that liked this article
    liked_by = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                      related_name='liked_articles',
                                      related_query_name='liked_article')
    # users that disliked this article
    disliked_by = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                         related_name='disliked_articles',
                                         related_query_name='disliked_article')

    class Meta:
        """Meta class difines extra functions to be ran on the DB
        'ordering = -created_at' ensures that the ordering of articles
        should in a descending order.
        """
        ordering = ['-created_at']

    def is_liked_by(self, user):
        """
        check if an article is liked by a user
        :param user: the user we are checking for
        :return: boolean, indicating whether or not the user liked the article
        """
        return user.liked_articles.filter(pk=self.pk).exists()

    def is_disliked_by(self, user):
        """
        check if an article is disliked by a user
        :param user: the user we are checking for
        :return: boolean: whether or not the user disliked the article
        """
        return user.disliked_articles.filter(pk=self.pk).exists()

    @property
    def like_count(self):
        return self.liked_by.count()

    @property
    def dislike_count(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title


def article_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    article_pre_save_reciever generates a unique slug for an article
    create_slug function cretes are slug based on the article title
    unique_random_string function generates a random string
    """
    slug = utils.create_slug(instance)
    random_string = utils.unique_random_string()
    if not instance.slug:
        instance.slug = f'{slug}-{random_string}'


pre_save.connect(article_pre_save_receiver, sender=Article)
