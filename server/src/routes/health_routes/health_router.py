from flask import Blueprint, jsonify
import config

health_router = Blueprint("health_router", __name__)

@health_router.route("/health", methods=["GET"])
def health():
    """"
    Endponint para evaluar estado del servidor
    """
    response = {
        "debug": config.DEBUG,
        "host": config.HOST,
        "message": "Activo",
        "port": config.PORT,
        "status": "success"
    }
    return jsonify(response), 200