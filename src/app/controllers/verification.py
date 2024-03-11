from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException, status
from typing import Annotated

from app.settings import default_storage_config as DSC

router = APIRouter(
    prefix='/verification',
    tags=['verify']
)

@router.post('/attached')
async def attached_signature(file: Annotated[UploadFile, File(description="File with attached signature")],):
    from app.services.files import save
    from app.tasks.verify import verify_by_path

    try:
        id = save([file.file], [file.filename])

        verify_by_path.apply_async(args=(DSC.path(id, file.filename),), task_id=id, countdown=0.5)

        return {'id': id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)


@router.post('/detached')
async def detached_signature(file: Annotated[UploadFile, File(description="File")],
                                  signature: Annotated[UploadFile, File(description="Signature")]):
    from app.services.files import save
    from app.tasks.verify import verify_by_path

    try:
        id = save([signature.file, file.file], [signature.filename, file.filename])

        verify_by_path.apply_async(args=(DSC.path(id, signature.filename), DSC.path(id, file.filename)),
                                    task_id=id, countdown=0.5)

        return {'id': id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)


@router.get('/id/{id}')
async def get_result_by_id(id: str):
    from celery.result import AsyncResult
    from celery import current_app

    res = AsyncResult(id, app=current_app)

    if not res.ready():
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail='not ready')

    if res.failed():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.result.args)

    if res.successful():
        return res.result
