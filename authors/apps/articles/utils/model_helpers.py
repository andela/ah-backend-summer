from rest_framework import status
from ..models import Article, Bookmark


def get_single_article_using_slug(slug):
    # This method will be used to get a single article using a slug
    # It will return none if there's no article in the DB with slug
    try:
        obj = Article.objects.get(slug=slug)
        return obj
    except Article.DoesNotExist:
        return None


def favorite_unfavorite_article(request, slug,
                                serializer_class, is_favoriting):
    """
    favorite_unfavorite_article returns either a dictionary with key of
    message indicating whether an article has been favorited or unfavorited,
    article which has been favorited or unfavorited and a status code of 200
    or it returns a dictionary with a key of errors with the appropriate status
    code
    """
    article = get_single_article_using_slug(slug)
    user = request.user.profile
    if article:
        Article.objects.toggle_favorite(user, article, is_favoriting)
        serializer = serializer_class(article,
                                      context={"request": request})
        title = article.title
        message = f"You have favorited this article {title}" if \
            is_favoriting else f"You have unfavorited this article {title}"
        data = {"message": message, "article": serializer.data}
        status_code = status.HTTP_200_OK
    else:
        data = {'errors': 'Article with this slug doesnot exist'}
        status_code = status.HTTP_404_NOT_FOUND
    return data, status_code


def get_all_available_tags():
    """
    This method returns all tags authors created if any
    """
    try:
        articles = Article.objects.all()
        articles_w_tags = [a for a in articles if a.tag_list]
        merged_tags_list = []
        if articles_w_tags:
            all_tags_list = [a.tag_list for a in articles_w_tags]
            for tag in all_tags_list:
                merged_tags_list += tag
            return set(merged_tags_list)
    except Article.DoesNotExist:
        return None


def get_all_articles_with_same_tag_name(tag_name):
    """
    This method returns all articles with the same tag name
    """
    articles_with_same_name = Article.objects.filter(
        tag_list__contains=[tag_name])
    if articles_with_same_name:
        return articles_with_same_name


def get_single_bookmark_user(article, user):
    """
    This method returns all bookmarks of a user
    """
    return Bookmark.objects.filter(article=article, user=user)


def get_single_bookmark_or_create_bookmark(article, user):
    """
    This method returns a bookmarks
    """
    try:
        obj = Bookmark.objects.get(article=article, user=user)
        return obj
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(article=article, user=user)
        return None
