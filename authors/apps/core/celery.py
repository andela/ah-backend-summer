from celery import Celery
from django.conf import settings

from authors.apps.core.utils import load_settings_file

load_settings_file()

app = Celery('authors', broker=settings.CELERY_BROKER)

# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# bind a task for debug logs
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
