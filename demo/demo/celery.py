from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

app = Celery('demo')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))