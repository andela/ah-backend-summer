"""
WSGI config for authors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""


from django.core.wsgi import get_wsgi_application

from authors.apps.core.utils import load_settings_file

load_settings_file()

application = get_wsgi_application()
