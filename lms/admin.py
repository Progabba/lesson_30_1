from celery import Celery
from celery.schedules import crontab

app = Celery("lms")

app.conf.beat_schedule = {
    "block-inactive-users-every-day": {
        "task": "lms.tasks.block_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # Запуск каждый день в полночь
    },
}
