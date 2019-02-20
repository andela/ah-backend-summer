"""
Register signal handlers from other apps that trigger notifications
"""
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from authors.apps.articles.signals import (
    article_published_signal,
    ArticlesSignalSender)
from authors.apps.comments.signals import (
    comment_published_signal,
    CommentsSignalSender,
    comment_liked_signal)
from authors.apps.notifications.models import Notification
from authors.apps.notifications.utils.messages import (
    article_published,
    comment_published,
    user_followed_message,
    comment_liked)
from authors.apps.profiles.signals import (
    followers_updated_signal,
    ProfilesSignalSender)


@receiver(article_published_signal, sender=ArticlesSignalSender)
def on_article_published(sender, **kwargs):
    """
    when an article is published, we want to create a notification for this
    and up queue the emails
    """
    article = kwargs['article']
    notification = Notification(title="New Article for You",
                                body=article_published.format(article=article))
    notification.save()
    notification.recipients.add(*article.author.followed_by.all())
    notification.queue_notification_emails()


@receiver(comment_liked_signal, sender=CommentsSignalSender)
def on_comment_liked(sender, **kwargs):
    """
    on_comment_liked creates a notification when user likes a comment and
    calls the function to send an email notification to the article author
    """
    user_model = kwargs.get("user_model")
    comment = kwargs.get("comment")
    user = get_object_or_404(user_model, id=kwargs.get("id"))
    notification = Notification(title="Comment Liked",
                                body=comment_liked.format(user=user,
                                                          comment=comment))
    notification.save()
    notification.recipients.add(comment.author)
    notification.queue_notification_emails()


@receiver(comment_published_signal, sender=CommentsSignalSender)
def on_new_comment_notify_people_that_favorited_article(sender, **kwargs):
    """
    when a comment is published, we want to create a notification for this
    and up queue the emails for people that favorited this article
    """
    comment = kwargs['comment']
    notification = Notification(
        title="New Comment on {article}".format(article=comment.article),
        body=comment_published.format(comment=comment))
    notification.save()
    recipients = comment.article.favorited_by.all()

    if comment.author in recipients:
        recipients.remove(comment.author)

    if comment.article.author in recipients:
        recipients.remove(comment.article.author)

    notification.recipients.add(*recipients)
    notification.queue_notification_emails()


@receiver(comment_published_signal, sender=CommentsSignalSender)
def on_new_comment_notify_article_author(sender, **kwargs):
    """
    when a comment is published, we want to create a notification for this
    and up queue the email for the author
    """
    comment = kwargs['comment']
    notification = Notification(
        title="New Comment on your {article}".format(article=comment.article),
        body=comment_published.format(comment=comment))
    notification.save()

    notification.recipients.add(comment.article.author)
    notification.queue_notification_emails()


@receiver(followers_updated_signal, sender=ProfilesSignalSender)
def on_follow_action_notify_followed_party(sender, **kwargs):
    """
    when a new person follows me, a notification is created and email queued
    """
    notification = Notification(
        title='Someone followed you',
        body=user_followed_message.format(
            username=kwargs['who_followed'].username,
            link_to_profile=kwargs[
                'who_followed'].url))
    notification.save()
    notification.recipients.add(kwargs['who_was_followed'])
    notification.queue_notification_emails()
