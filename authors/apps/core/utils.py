import os

from dotenv import find_dotenv, load_dotenv


def load_settings_file():
    # load environment variables from an optional .env file
    load_dotenv(find_dotenv())

    environment = os.environ.get('ENVIRONMENT', 'production')
    if environment == 'development':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "authors.settings.development")
    elif environment == 'staging':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "authors.settings.staging")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "authors.settings.production")
