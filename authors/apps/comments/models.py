from django.conf import settings

from django.db import models
from rest_framework.reverse import reverse

from simple_history.models import HistoricalRecords

from ..profiles.models import Profile
from ..articles.models import Article


class Comment(models.Model):
    """The model defines the Comments table as stored in the DB
    """
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    edit_history = HistoricalRecords()

    class Meta:
        """
        Ensure that the comments are returned in the order they were created
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.body

    def comment_is_my_own(self):
        return self.author == self.article.author

    @property
    def url(self):
        return settings.URL + reverse('comments:comment-details',
                                      kwargs={"pk": self.pk})


class CommentReply(models.Model):
    """The model defines the Comment-Replies table as stored in the DB
    """
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    edit_history = HistoricalRecords()

    class Meta:
        """
        Ensure that the comment-replies are returned in the order they were
        created
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.body

    @property
    def url(self):
        return settings.URL + reverse('comments:comment-reply-details',
                                      kwargs={"pk": self.pk})
