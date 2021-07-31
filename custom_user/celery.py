import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'custom_user.secrets')

app = Celery('custom_user')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
