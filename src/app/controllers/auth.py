from fastapi import APIRouter, UploadFile, File, Depends, Request, Response, Cookie, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated, Optional
from app.configuration.auth import check_auth, COOKIE_SESSION_ID_KEY, set_session_data, get_session_data, drop_session_data, TTL

router = APIRouter(
    prefix='/auth',
    tags=['authentification']
)

@router.post("/login")
def login(response: Response, auth: Annotated[str, Depends(check_auth)], session_id: Annotated[str, Depends(set_session_data)]):
    
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id, expires=TTL, samesite='strict')
    return {"success": True}


@router.get("/check")
def check_cookie(session_data: Annotated[str, Depends(get_session_data)]):
    return session_data


@router.get("/logout")
def logout(response: Response, droped_session: Annotated[str, Depends(drop_session_data)]):
    
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    
    return {'deleted': droped_session}