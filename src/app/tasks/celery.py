from celery import current_app as current_celery_app, Task
from app.settings import default_celery_config
from celery.schedules import crontab


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(default_celery_config, namespace="CELERY")
    celery_app.conf.beat_schedule = {
        'clean-old-files-every-day': {
            'task': 'app.tasks.garbage.run_gc',
            'schedule': crontab(minute='0', hour='0', day_of_week='*/1')
        },
    }

    return celery_app
