import os

from celery import Celery
from celery.schedules import crontab
import yapis.settings

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yapis.settings')

app = Celery('yapis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.beat_schedule ={
    'periodic youtube data fetch':{
        'task':'videosapp.tasks.youtube_task',
        'schedule': crontab(minute='*/5')
    }
}

INSTALLED_APPS = yapis.settings.INSTALLED_APPS

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: INSTALLED_APPS)




