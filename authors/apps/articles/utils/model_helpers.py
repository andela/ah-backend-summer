from ..models import Article


def get_single_article_using_slug(slug):
    # This method will be used to get a single article using a slug
    # It will return none if there's no article in the DB with slug
    try:
        obj = Article.objects.get(slug=slug)
        return obj
    except Article.DoesNotExist:
        return None
