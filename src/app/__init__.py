from typing import Any, Tuple

from fastapi import FastAPI

from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
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

    app.add_middleware(GZipMiddleware, minimum_size=100)
    
    app.add_middleware(
            CORSMiddleware,
            allow_origins=['http://localhost:5173'], # Vite
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH"],
            allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"]
    )
    celery_app = create_celery()

    return Server(app).get_app(), celery_app
