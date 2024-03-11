from typing import BinaryIO, Iterable
from os import listdir, mkdir, path, unlink
from shutil import copyfileobj, rmtree
from uuid import uuid4
from os.path import getmtime
from datetime import datetime as dt, timedelta as td

from app.settings import default_storage_config as DSC

def save(files: Iterable[BinaryIO], names: Iterable[str]) -> str:
    id: str = uuid4().hex

    while path.isdir(DSC.path(id)):
        id = uuid4().hex
    
    mkdir(DSC.path(id))

    for file, name in zip(files, names):
        with open(DSC.path(id, name), 'wb') as fw:
            copyfileobj(file, fw)
        file.close()
    
    return id

def clean_garbage(unmodified_hours: float = 24.) -> int:
    if unmodified_hours < 0:
        raise Exception("negative hours")
    
    try:
        dirs = listdir(DSC.path())
        times = [(_dir, dt.fromtimestamp(getmtime(DSC.path(_dir)))) for _dir in dirs]

        mapped = map(lambda tpl: rmtree(DSC.path(tpl[0])), filter(lambda tpl: dt.now() - tpl[1] > td(hours=unmodified_hours), times))

        return len([m for m in mapped])

    except Exception as e:
        raise e