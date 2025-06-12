from flask import Blueprint, jsonify, request
from ...services.format_recognition.format_recognition import FormatRecognitionService
from ...services.pdf_extractor.pdf_extractor import PDFExtractorService
from ...services.image_extractor.image_extractor import ImageExtractorService




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
        # Llama la función que identifica el formato
        file_info = FormatRecognitionService.format_recognition(file)
        # Extracte el formato
        file_type = file_info.get("category")
        processed_data = None
        message_suffix = ""
        file.seek(0)
        # Verifica si es PDF
        if file_type == "pdf":
            processed_data = PDFExtractorService.pdf_extract(file)
            message_suffix = "procesado como PDF"
        # Verifica si es imagen 
        elif file_type == "image":
            processed_data = ImageExtractorService.image_extract(file)
            message_suffix = "procesado como imagen"
        # Verifica si es Word
        elif file_type == "word":
            message_suffix = "procesado como Word"
        # Verifica si es otro tipo de archivo
        else:
            message_suffix = "no procesado"
        # Respuesta para el cliente
        response = {
            "file_info": file_info,
            "message": "Archivo recbido y " + message_suffix,
            "processed_data": processed_data, # Respueta del servicio de procesamiento
            "status": "success",
        }
        return jsonify(response), 200
    except Exception as e:
        response = {"message": str(IOError), "status": "error"}
        return jsonify(response), 500
