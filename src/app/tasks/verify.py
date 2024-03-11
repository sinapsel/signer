from celery import shared_task
from typing import Mapping

@shared_task
def verify_by_path(sig_path: str, path: str|None = None):
    from app.services.gpg import verify

    try:
        res = verify(sig_path, path)
        return res
    except Exception as e:
        raise e

