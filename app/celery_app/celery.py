from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("tms")
app.conf.broker_url = REDIS_URL
app.conf.result_backend = REDIS_URL
app.autodiscover_tasks(["app.celery_app", "app.api"])
