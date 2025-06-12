# Importando Blueprints
from ..routes.health_routes.health_router import health_router

def register_blueprints(app):
    """
    Blueprints del API de Flask
    """ 
    app.register_blueprint(health_router)