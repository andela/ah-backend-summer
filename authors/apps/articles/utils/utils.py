import random
import string

from django.utils.text import slugify

def unique_random_string(size=7):
	chars=string.ascii_lowercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))

def create_slug(instance):
	return slugify(instance.title)
