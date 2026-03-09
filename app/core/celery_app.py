from celery import Celery

from app.utils.settings import settings

celery_app = Celery(
    "todo_workers",
    broker= settings.CELERY_REDIS_URL,
    backend= settings.CELERY_BACKEND_REDIS_URL,
    include=["app.tasks.email_task"]
)

celery_app.conf.update(
    broker_pool_limit=2,
    broker_connection_retry_on_startup=True,
    task_track_started = True,
    worker_send_task_events=True,   # <-- REQUIRED
    task_send_sent_event=True,       # <-- also useful
    result_expires=3600
)

print("BROKER:", settings.CELERY_REDIS_URL)
print("BACKEND:", settings.CELERY_BACKEND_REDIS_URL)