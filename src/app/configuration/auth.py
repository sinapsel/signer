from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, status, HTTPException, Security, Cookie
from app.settings import AdminCredentials, get_admin_credentials
from typing import Annotated
from hashlib import md5
from uuid import uuid4
from app.services.redis import get_db, RedisDB
import secrets
from time import time
import json
import re

security = HTTPBasic()

COOKIE_SESSION_ID_KEY = 'SIGNER-AUTH'

TTL = 120

def check_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                correct_credentials: Annotated[AdminCredentials, Depends(get_admin_credentials)]):
    login = credentials.username.encode("utf8")
    passw = md5(credentials.password.encode("utf8")).hexdigest().encode('utf-8')


    is_correct = secrets.compare_digest(login, correct_credentials.login) and\
          secrets.compare_digest(passw, correct_credentials.passw)

    if not is_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

def generate_session_id() -> str:
    session_id: str = f'auth-key-{uuid4().hex}'
    return session_id


def get_session_data(db: Annotated[RedisDB, Depends(get_db)],
                        session_id: str = Cookie(default=None, alias=COOKIE_SESSION_ID_KEY)) -> str:
    
    exc = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Not authenticated",
        )
    
    if not session_id:
        raise exc

    if re.match(r'auth-key-[a-z0-9]{32}', session_id) is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if session_id not in db:
        raise exc

    return db[session_id]


def set_session_data(db: Annotated[RedisDB, Depends(get_db)]) -> str:
    session_id = generate_session_id()
    while session_id in db:
        session_id = generate_session_id()


    db[session_id:TTL] = json.dumps({
        'auth_time': time(),
    })
    
    return session_id

def drop_session_data(db: Annotated[RedisDB, Depends(get_db)], session_data: str = Depends(get_session_data), 
                        session_id: str = Cookie(default=None, alias=COOKIE_SESSION_ID_KEY)) -> int:    
    del db[session_id]

    return session_id