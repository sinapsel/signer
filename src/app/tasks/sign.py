from celery import shared_task
from typing import Mapping

@shared_task
def sign_by_path(attribs: Mapping[str, str]):
    from app.services.gpg import sign

    try:
        res = sign(**attribs)
        return res
    except Exception as e:
        raise e

