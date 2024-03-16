from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Optional
from app.models.sign import SignAttribsFull, SignKind
from os.path import split as pathsplit
from hashlib import md5
from app.configuration.auth import get_session_data

from app.settings import default_storage_config as DSC

router = APIRouter(
    prefix='/signature',
    tags=['sign']
)



@router.post('')
async def sign(file: Annotated[UploadFile, File(description="File to sign")],
               user: Annotated[str, Form()],
               pin: Annotated[str, Form()],
               kind: Optional[SignKind] = Form(SignKind.detached),
               ascii: Optional[bool] = Form(None),
               fixFileExists: Optional[bool] = Form(None),
               auth: Optional[bool] = Depends(get_session_data)
            ):
    from app.services.files import save
    from app.tasks.sign import sign_by_path

    try:
        id = save([file.file], [file.filename])

        attribs = SignAttribsFull(
            path = DSC.path(id, file.filename), user=user, pin=pin, kind=kind,
            ascii=ascii, fixFileExists=fixFileExists
        )

        sign_by_path.apply_async(args=(attribs.dict(),), task_id=id, countdown=5)

        return {'id': id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)


@router.get('/id/{id}')
async def get_result_by_id(id: str, download: bool = False, download_source: bool = False, auth: Optional[bool] = Depends(get_session_data)):
    from celery.result import AsyncResult
    from celery import current_app

    res = AsyncResult(id, app=current_app)

    if not res.ready():
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail='not ready')

    if res.failed():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            'error': res.result.__class__.__name__,
            'info': res.result.args
        })

    if res.successful():
        signed_path = pathsplit(res.result.get('singed_path'))[1]
        source_path = pathsplit(res.result.get('path'))[1]

        if download:
            return FileResponse(path=res.result.get('singed_path'), filename=signed_path,
                            media_type="application/octet-stream")
        if download_source:
            return FileResponse(path=res.result.get('path'), filename=source_path,
                            media_type="application/octet-stream")
        return {'success': True, 'download': signed_path, 'download_source': source_path}
