from django.db.models.signals import (
    post_save, m2m_changed as model_field_changed_signal)
from django.dispatch import receiver, Signal

from authors.apps.comments.models import Comment


# custom signal we shall send when a comment is published
# the rationale for this custom signal is discussed in the articles app
comment_published_signal = Signal(providing_args=["comment"])
comment_liked_signal = Signal(
    providing_args=["comment", "user_model", "id"]
    )


class CommentsSignalSender:
    pass


@receiver(post_save, sender=Comment)
def on_comment_post_save(sender, **kwargs):
    if kwargs['created']:
        comment_published_signal.send(CommentsSignalSender,
                                      comment=kwargs['instance'])


@receiver(model_field_changed_signal, sender=Comment.liked_by.through)
def on_like_comment(sender, **kwargs):
    """
    on_like_comment is run when a user likes a comment. Then calls a signal
    to notify the user
    """
    comment = kwargs.get("instance")
    user_model = kwargs.get("model")
    action = kwargs.get("action")
    pk_set = kwargs.get("pk_set")
    if action == "post_add":
        user_id = [pk for pk in pk_set]
        comment_liked_signal.send(CommentsSignalSender,
                                  comment=comment,
                                  user_model=user_model,
                                  id=user_id[0])
