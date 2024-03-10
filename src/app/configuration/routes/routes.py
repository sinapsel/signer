from fastapi import FastAPI
from dataclasses import dataclass
from app.settings import ControllersConfig
from typing import Iterable


@dataclass(frozen=True)
class Routes:
    routers: Iterable

    def register(self, app: FastAPI) -> None:
        list(map(lambda route: app.include_router(route), self.routers))

    @classmethod
    def autoresolve(cls, config: ControllersConfig) -> tuple[__module__]:
        import re 
        from os import listdir
        
        module_names = [re.sub(r'.py$', '', mod) for mod in filter(lambda x: re.match(r'^[^_](.+).py$', x),
                                     listdir(config.load_path))]

        _module = __import__(config.import_path, fromlist=module_names)
                
        routers = tuple(getattr(mod, 'router') for mod in (getattr(_module, mod) for mod in module_names))

        return routers