release: python manage.py migrate
worker: celery -A authors.apps.core worker -l error --without-gossip --without-mingle --without-heartbeat
web: gunicorn authors.wsgi --log-file -
heroku ps:scale worker=1
