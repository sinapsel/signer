from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SignKind(str, Enum):
    attached = '--sign'
    detached = '--detach-sign'
    clear = '--clear-sign'

class SignAttribs(BaseModel):
    user: str
    pin: str
    kind: Optional[SignKind] = SignKind.detached
    ascii: Optional[bool] = False
    fixFileExists: Optional[bool] = False

class SignAttribsFull(SignAttribs):
    path: str