"""Signal dispatchers and handlers for the articles module"""
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from authors.apps.articles.models import Article

# our custom signal that will be sent when a new article is published
# we could have stuck to using the post_save signal and receiving it in the
# notifications app or calling one of the util methods there,
# but that kills the whole benefit to the modularity we're going for
article_published_signal = Signal(providing_args=["article"])


class ArticlesSignalSender:
    pass


@receiver(post_save, sender=Article)
def on_article_post_save(sender, **kwargs):
    """called when an article is saved"""
    if kwargs['created']:
        # we are only acting when something we are interested in
        # actually happened
        article_published_signal.send(ArticlesSignalSender,
                                      article=kwargs['instance'])
