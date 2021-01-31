from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from src.quick_check.settings import CELERY_APPS
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.quick_check.settings')

app = Celery('quick_check')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: CELERY_APPS)
app.conf.update(
    timezone='Europe/Moscow'
)

app.conf.beat_schedule = {
    'generate_codes': {
        'task': 'src.apps.celery.tasks.update_neuro_data',
        # 'schedule': crontab(hour='*/24'),
        'schedule': crontab(minute='*/1'),
    },

}
