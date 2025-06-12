from flask import Flask
from flask_cors import CORS
import config

# Importando otros modulos
from src.routes.main_router import register_blueprints

# Iniciando aplicación Flask
app = Flask(__name__)
CORS(app)

# Importando Blueprints
register_blueprints(app)

if __name__ == "__main__":
    app.run(host=str(config.HOST), port=config.PORT, debug=True)
