import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')

app = Celery('LMS')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'relay-outbox-events-every-5-seconds': {
        'task': 'apps.payroll.tasks.publish_outbox_events',
        'schedule': 5.0,
    },
}