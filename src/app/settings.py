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
class ControllersConfig:
    PATH = ['app', 'controllers']

    @property
    def import_path(self):
        return '.'.join(self.PATH)
    
    @property
    def load_path(self):
        return '/'.join(self.PATH)


default_celery_config = CeleryConfig()
default_controllers_config = ControllersConfig()
