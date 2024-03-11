import logging
from dataclasses import dataclass
import os
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')



@dataclass(frozen=True)
class CeleryConfig:
    CELERY_BROKER_URL: str = "{engine}://{host}:{port}/0".format(engine='redis',
                                                                 host=REDIS_HOST,
                                                                 port=REDIS_PORT)
    CELERY_RESULT_BACKEND: str = "{engine}://{host}:{port}/0".format(engine='redis',
                                                                     host=REDIS_HOST,
                                                                     port=REDIS_PORT)
    CELERY_IMPORTS: tuple[str] = ("app.tasks.sign", 'app.tasks.verify', 'app.tasks.garbage')

    result_extended: bool = True

    task_serializer = "json"
    result_serializer = "json"
    event_serializer = "json"
    accept_content = ["application/json"]
    result_accept_content = ["application/json"]


@dataclass(frozen=True)
class ControllersConfig:
    PATH = ['app', 'controllers']

    @property
    def import_path(self):
        return '.'.join(self.PATH)
    
    @property
    def load_path(self):
        return os.path.join(*self.PATH)
    
@dataclass(frozen=True) 
class StoragePathConfig:
    PATH = ['storage']

    def path(self, *args):
        return os.path.join(*self.PATH, *args)

@dataclass(frozen=True)
class AdminCredentials:
    login: bytes = os.getenv('LOGIN_ADMIN', '').encode('utf-8')
    passw: bytes = os.getenv('PASSW_ADMIN', '').encode('utf-8')

default_celery_config = CeleryConfig()
default_controllers_config = ControllersConfig()
default_storage_config = StoragePathConfig()

def get_admin_credentials():
    return AdminCredentials()