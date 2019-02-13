import random
import string
import readtime

from django.utils.text import slugify
from django.db.models import Avg


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
