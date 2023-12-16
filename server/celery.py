import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')


app = Celery('server')
app.config_from_object(settings.CELERY)  # type: ignore
app.autodiscover_tasks()


app.conf.beat_schedule = {}
