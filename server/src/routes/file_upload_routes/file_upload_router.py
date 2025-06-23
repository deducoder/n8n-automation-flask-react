from flask import Blueprint, jsonify, request
from decouple import config
import requests

from ...services.format_recognition.format_recognition import FormatRecognitionService
from ...services.pdf_extractor.pdf_extractor import PDFExtractorService
from ...services.image_extractor.image_extractor import ImageExtractorService
from ...services.word_extractor.word_extractor import DocumentExtractorService


file_upload_router = Blueprint("file_upload_router", __name__)

# n8n Webhook URL
N8N_WEBHOOK_URL = str(config("N8N_WEBHOOK_URL",  default=""))

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
    
    # Variables de almacenamiento de datos procesados y respuestas de n8n
    processed_data = None
    extracted_text_from_file = None
    n8n_response_data = None
    message_suffix = ""
    
    # Identifica tipo de archivo
    try:
        # Llama la función que identifica el formato
        file_info = FormatRecognitionService.format_recognition(file)
        # Extracte el formato
        file_type = file_info.get("category")
        # Reinicia posición del puntero
        file.seek(0)
        
        # Verifica si es PDF
        if file_type == "pdf":
            processing_result = PDFExtractorService.pdf_extract(file)
            if processing_result and processing_result.get("status") == "success":
                processed_data = processing_result
                extracted_text_from_file = processing_result.get("extracted_text")
                message_suffix = "procesado como PDF"
            else:
                raise Exception(processing_result.get("message", "Error al procesar el archivo"))

        # Verifica si es imagen 
        elif file_type == "image":
            processing_result = ImageExtractorService.image_extract(file)
            if processing_result and processing_result.get("status") == "success":
                processed_data = processing_result
                extracted_text_from_file = processing_result.get("extracted_text")
                message_suffix = "procesado como imagen"
            else:
                raise Exception(processing_result.get("message", "Error al procesar el archivo"))

        # Verifica si es Word
        elif file_type == "word":
            processing_result = DocumentExtractorService.docx_extract(file)
            if processing_result and processing_result.get("status") == "success":
                processed_data = processing_result
                extracted_text_from_file = processing_result.get("extracted_text")
                message_suffix = "procesado como Word"
            
        # Verifica si es otro tipo de archivo
        else:
            message_suffix = "no procesado"
        
        # Envía y recibe datos a n8n para procesamiento
        if extracted_text_from_file and N8N_WEBHOOK_URL:
            body = {
                "extracted_text": extracted_text_from_file, # Texto que n8n procesará
                "fileile_info": file_info, # Información básica del archivo
                "original_file_name": file.filename, # Nombre original del archivo
            }
            # Realiza petición POST a n8n
            n8n_response = requests.post(N8N_WEBHOOK_URL, json=body)
            # Verifica la petición HTTP 
            n8n_response.raise_for_status()
            # Obtiene respuesta de n8n
            n8n_response_data = n8n_response.json()
            # print(f"Respuesta de n8n: {n8n_response_data}")
            message_suffix += " y enviado a n8n"
        elif not N8N_WEBHOOK_URL:
            message_suffix = ". n8n URL no configurada"
        
        # Respuesta para el cliente
        response = {
            "file_info": file_info,
            "message": "Archivo recbido, " + message_suffix,
            "n8n_response": n8n_response_data, # Respuesta de n8n
            "processed_data": processed_data, # Respueta del servicio de procesamiento
            "status": "success",
        }
        return jsonify(response), 200
    
    except Exception as e:
        response = {"message": str(IOError), "status": "error"}
        return jsonify(response), 500
