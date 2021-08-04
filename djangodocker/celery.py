import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangodocker.settings")

app = Celery("djangodocker")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "populate_driver_data": {
        "task": "drivers.tasks.populate_driver_data",
        "schedule": crontab(minute=0, hour=0),
    },
    "populate_driver_metric_data": {
        "task": "drivers.tasks.log_driver_twitter_metric",
        "schedule": crontab(minute="*/60"),
    },
}
