import os
import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

django.setup()
celery_app = Celery("habit_tracker")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")


celery_app.conf.beat_schedule = {
    'send-habit-reminders': {
        'task': 'habits.tasks.send_habit_reminder',
        'schedule': crontab(minute='*', hour='*'),  # каждая минута
    },
}

celery_app.autodiscover_tasks()