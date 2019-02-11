from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from ..profiles import models as ProfileModel
from .utils import utils

from ..authentication.models import User
from .utils.utils import get_average_rate


class ArticleManager(models.Manager):
    """
    ArticleManager class is a custom Article model manager
    """

    def toggle_favorite(self, user, article):
        """
        toggle_favorite method adds user to favorited_by if they favorite an
        article or removes user from favorited_by if the unfavorite an article
        """
        if user in article.favorited_by.all():
            article.favorited_by.remove(user)
            message = "You have unfavorited this article"
        else:
            article.favorited_by.add(user)
            message = "You have favorited this article"
        article.favoritesCount = article.favorited_by.all().count()
        article.save()
        return message


class Article(models.Model):
    """The Article class model defines the Article table model in the DB
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    favorited_by = models.ManyToManyField(ProfileModel.Profile,
                                          blank=True,
                                          related_name="favorited_by")
    favoritesCount = models.IntegerField(default=0)
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

    objects = ArticleManager()

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
        return self.disliked_by.count()

    def __str__(self):
        return self.title

    @property
    def average_ratings(self):
        """
        Calculates average of a reviewed article
        Returns: average rate score
        """
        return get_average_rate(
            model=Rating,
            article=self.pk
        )


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


class Rating(models.Model):
    """
    Authenticated users can rate an article on a scale of 1 to 5
    Users can get average rating for every article
    """
    rate_score = models.IntegerField(null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='article_ratings',
                                blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
