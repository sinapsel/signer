from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from typing import Annotated


router = APIRouter(
    prefix='/verification',
    tags=['verify']
)

@router.api_route('/attached', methods=['POST'])
async def attached_signature(request: Request, file: Annotated[UploadFile, File(description="File with attached signature")],):
    ...

@router.api_route('/detached', methods=['POST'])
async def detached_signature(request: Request, file: Annotated[UploadFile, File(description="File")],
                                  signature: Annotated[UploadFile, File(description="Signature")]):
    ...
