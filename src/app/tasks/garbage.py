from celery import shared_task
from typing import Mapping

@shared_task
def run_gc(hours: float = 24.):
    from app.services.files import clean_garbage

    return clean_garbage(hours)