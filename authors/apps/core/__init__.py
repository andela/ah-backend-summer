# this basically avoids the problem of the `celery.py` file being confused
# for the main celery module
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

# the entire __init__.py file is loaded by default, (from .__init__ import *)
# when python enters a module.
# this says, please load only these objects
# and allows us to use the `@shared_task` decorator in `tasks.py` in other apps
__all__ = ('celery_app',)
