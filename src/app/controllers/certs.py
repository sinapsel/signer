from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated, Optional

router = APIRouter(
    prefix='/certs',
    tags=['certificates']
)

@router.get('/all/')
async def get_all(public: Annotated[bool, 'List only public keys'] = True):
    from app.services.gpg import list_keys

    return list_keys(public=public)

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
        return StreamingResponse(chunker(cert))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args)