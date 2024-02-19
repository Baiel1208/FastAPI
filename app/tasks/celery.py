from celery import Celery

from app.config import settings


celery = Celery(
    'tasks',
    broker=f"redis://{settings.REIDS_HOST}:{settings.REIDS_PORT}",
    include=['app.tasks.tasks']
)
