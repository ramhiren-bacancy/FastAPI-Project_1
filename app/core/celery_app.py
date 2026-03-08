from celery import Celery

celery_app = Celery(
    "todo_workers",
    broker="redis://default:bHWOOr7NokDLg7IzdD0qRkcG6vPkNdHQ@redis-18294.crce182.ap-south-1-1.ec2.cloud.redislabs.com:18294/0",
    backend="redis://default:bHWOOr7NokDLg7IzdD0qRkcG6vPkNdHQ@redis-18294.crce182.ap-south-1-1.ec2.cloud.redislabs.com:18294/0",
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

