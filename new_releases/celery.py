from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

PROJECT_NAME='app'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
# app.conf.enable_utc = False # so celery doesn't take utc by default
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
