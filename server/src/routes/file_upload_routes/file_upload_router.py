from flask import Blueprint, jsonify, request
from ...services.format_recognition.format_recognition import FormatRecognitionService


file_upload_router = Blueprint("file_upload_router", __name__)


@file_upload_router.route("/file_upload", methods=["POST"])
def file_upload():
    """
    Endpoint para recibir los archivos desde el cliente
    """
    # Valida envió del archivo
    if "file" not in request.files:
        response = {"message": "No se encontro el archivo", "status": "error"}
        return jsonify(response), 400
    # Almamcena el archivo
    file = request.files["file"]
    # Valida el nombre del archivo
    if file.filename == "":
        response = {"message": "Nombre de archivo invalido", "status": "error"}
        return jsonify(response), 400
    # Identifica tipo de archivo
    try:
        file_info = FormatRecognitionService.format_recognition(file)
        response = {
            "file_info": file_info,
            "message": "Archivo recbido e identificado",
            "status": "success",
        }
        return jsonify(response), 200
    except Exception as e:
        response = {"message": str(e), "status": "error"}
        return jsonify(response), 500
