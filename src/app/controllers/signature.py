from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Optional
from app.models.sign import SignAttribsFull, SignKind
from os.path import split as pathsplit
from hashlib import md5
import secrets

from app.settings import default_storage_config as DSC, AdminCredentials, get_admin_credentials

router = APIRouter(
    prefix='/signature',
    tags=['sign']
)

security = HTTPBasic()

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

@router.post('')
async def sign(file: Annotated[UploadFile, File(description="File to sign")],
               user: Annotated[str, Form()],
               pin: Annotated[str, Form()],
               kind: Optional[SignKind] = Form(SignKind.detached),
               ascii: Optional[bool] = Form(None),
               fixFileExists: Optional[bool] = Form(None),
               auth: Optional[bool] = Depends(check_auth)
            ):
    from app.services.files import save
    from app.tasks.sign import sign_by_path

    try:
        id = save([file.file], [file.filename])

        attribs = SignAttribsFull(
            path = DSC.path(id, file.filename), user=user, pin=pin, kind=kind,
            ascii=ascii, fixFileExists=fixFileExists
        )

        sign_by_path.apply_async(args=(attribs.dict(),), task_id=id, countdown=0.5)

        return {'id': id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)


@router.get('/id/{id}')
async def get_result_by_id(id: str, auth: Optional[bool] = Depends(check_auth)):
    from celery.result import AsyncResult
    from celery import current_app

    res = AsyncResult(id, app=current_app)

    if not res.ready():
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail='not ready')

    if res.failed():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.result.args)

    if res.successful():
        return FileResponse(path=res.result.get('singed_path'), filename=pathsplit(res.result.get('singed_path'))[1],
                            media_type="application/octet-stream")
