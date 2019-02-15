from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from authors.apps.comments.models import Comment


# custom signal we shall send when a comment is published
# the rationale for this custom signal is discussed in the articles app
comment_published_signal = Signal(providing_args=["comment"])


class CommentsSignalSender:
    pass


@receiver(post_save, sender=Comment)
def on_comment_post_save(sender, **kwargs):
    if kwargs['created']:
        comment_published_signal.send(CommentsSignalSender,
                                      comment=kwargs['instance'])
