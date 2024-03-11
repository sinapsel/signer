from typing import Any, Tuple

from fastapi import FastAPI

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.configuration.server import Server
from app.tasks.celery import create_celery

general_description = """
Web-service example on signing and verifying files using GnuPG
"""


def create_app(_=None) -> Tuple[FastAPI, Any]:
    app = FastAPI(
        title='Signer Tool',
        description=general_description,
        version='0.0.1',
        servers=[{'url': '/api'}],
        root_path='/api',
        root_path_in_servers=False,
        openapi_url='/docs/openapi.json',
        redoc_url=None,
        docs_url='/swagger'
    )

    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["localhost"]
    )
    celery_app = create_celery()

    return Server(app).get_app(), celery_app
