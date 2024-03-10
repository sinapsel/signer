from fastapi import FastAPI
from app.configuration.routes import __routes__


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def __register_events(app: FastAPI):
        app.on_event('startup')()

    @staticmethod
    def __register_routes(app: FastAPI):
        __routes__.register(app=app)
