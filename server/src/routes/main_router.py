# Importando Blueprints
from ..routes.health_routes.health_router import health_router
from ..routes.file_upload_routes.file_upload_router import file_upload_router

# Registrando Blueprints

def register_blueprints(app):
    """
    Blueprints del API de Flask
    """ 
    app.register_blueprint(health_router)
    app.register_blueprint(file_upload_router)