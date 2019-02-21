import random
import string
import readtime

from django.utils.text import slugify
from django.db.models import Avg
from django.urls import reverse
from urllib.parse import quote


def unique_random_string(size=7):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def create_slug(instance):
    return slugify(instance.title)


def get_average_rate(**kwargs):
    average_ratings = kwargs.get('model').objects.all().filter(
        article=kwargs.get('article')).aggregate(
            Avg('rate_score')).get('rate_score__avg')
    if average_ratings is None:
        return 0
    else:
        return int(average_ratings)


def get_article_read_time(body):
    """
    Calculates the time some article takes the average human to read,
    based on Medium’s read time formula.

    Based on research, people are able to read English at 200 WPM
    on paper, and 180 WPM on a monitor.
    Read time is based on the average reading speed of an adult
    (roughly 275 WPM). We take the total word count of a post
    and translate it into minutes. Then, we add 12 seconds
    for each inline image.

    Parameters: Body of the article
    Returns: average read time of an article

    """
    if body:
        result = readtime.of_text(body)
        return str(result)
    else:
        return "0 min read"


def get_articles_url(obj, request):
    url = request.build_absolute_uri(reverse('articles:article-details',
                                             kwargs={
                                                 'slug': obj.article.slug
                                             }))
    return url


def get_sharing_links(obj, request):
    """
    This method creates links that will be used to post an article to
    Facebook and Google Plus, or share an article as a tweet on Twitter
    and also share the article through email to another email user

    Parameters: Request of the body and the article object
    Returns: share links for platforms of social media and email

    """
    share_links = dict()
    url = request.build_absolute_uri(reverse('articles:article-details',
                                             kwargs={'slug': obj.slug}))
    title = quote(obj.title)
    author = quote(obj.author.username)
    space = quote(' ')
    append_to_url = f'{title}{space}by{space}{author}{space}{url}'

    share_links['google_plus'] = f"https://plus.google.com/share?url\
={url}"
    share_links['twitter'] = f"https://twitter.com/home?status={append_to_url}"
    share_links['facebook'] = f"https://www.facebook.com/sharer/sharer.php?u\
={url}"

    message = quote('I am sharing this article, ')
    body = (f"""{message}'{title}'%20{url}""")
    share_links['email'] = f'mailto:?&subject={title}&body={body}'

    return share_links
