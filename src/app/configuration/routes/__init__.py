from app.configuration.routes.routes import Routes
from app.settings import default_controllers_config


__routes__ = Routes(routers=Routes.autoresolve(default_controllers_config))

