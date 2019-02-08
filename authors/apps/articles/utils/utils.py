import random
import string

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
