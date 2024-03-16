from fastapi import APIRouter, UploadFile, File, Depends, Security, Request, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated, Optional
from app.configuration.auth import get_session_data

router = APIRouter(
    prefix='/certs',
    tags=['certificates']
)

@router.get('/all')
async def get_all():
    from app.services.gpg import list_keys

    return list_keys(public=True)

@router.get('/private')
async def get_private(session_data: Annotated[str, Depends(get_session_data)]):
    from app.services.gpg import list_keys

    return list_keys(public=False)

async def chunker(resourse: bytes, chunk: int = 128):
    for i in range(0, len(resourse), chunk):
        yield resourse[i:i+chunk]

@router.get('/uid/{uid}')
async def get_by_uid(uid: str, ascii: Optional[bool] = None):
    from app.services.gpg import export

    try:
        cert = export(uid, ascii)
        if not len(cert):
            raise Exception('key not found')
        return StreamingResponse(chunker(cert), media_type='application/octet-stream', 
                                 headers={'Content-Disposition': f'inline; filename="{uid}.crt"'})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)