from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery

from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess.settings')

app = Celery('mess')
app.conf.enable_utc = False # 
app.conf.update(timezone = 'Asia/Dhaka')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.s
app.config_from_object(settings, namespace='CELERY')
# app.config_from_object('django.conf:settings', namespace='CELERY')  



# Celery Beat
app.conf.beat_schedule = {
    'check_mess_update_times': {
        'task': 'webapp.tasks.update_next_day_meal',
        'schedule': crontab(minute='*'),  # Runs every minute
    },
}




# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True) #
# @app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')