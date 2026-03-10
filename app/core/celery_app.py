from celery import Celery

from app.utils.settings import settings

celery_app = Celery(
    "todo_workers",
    broker= settings.CELERY_REDIS_URL,
    backend= settings.CELERY_BACKEND_REDIS_URL,
    include=["app.tasks.email_task"]
)

celery_app.conf.update(
    task_default_queue="celery",
    task_default_exchange="celery",
    task_default_routing_key="celery",
    result_expires=3600
)

celery_app.autodiscover_tasks(["app"])

print("BROKER:", settings.CELERY_REDIS_URL)
print("BACKEND:", settings.CELERY_BACKEND_REDIS_URL)