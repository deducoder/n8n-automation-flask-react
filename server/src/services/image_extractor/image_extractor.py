from email.mime import image
from unittest import result
import easyocr
import numpy as np
from PIL import Image
import io

# Define los idiomas
reader = easyocr.Reader(['es'])

class ImageExtractorService:
    @staticmethod
    def image_extract(file):
        """
        Procesa una imagen para EasyOCR para extraer el texto
        """
        try:
            # Convierte el File a un Objeto BytesIO
            image_bytes = io.BytesIO(file.read())
            image = Image.open(image_bytes).convert("RGB")
            # Convierte la imagen PIL a un array de NumPy
            image_np = np.array(image)
            # Realiza reconocimiento de texto en la imagen
            results = reader.readtext(image_np)
            # Une todo el texto
            extracted_text = "\n".join([text for (bbox, text, prob) in results])
            # Retorna los resultados de la extracción
            return {
                "extracted_text": extracted_text,
                "message": "Texto extraído correctamente",
                "status": "success"
            }
        except Exception as e:
            # Captura error inesperado
            print(f"Error inesperado al procesar la imagen: {e}")
            return {
                "extracted_text": None,
                "status": "error",
                "message": f"Ocurrió un error inesperado al procesar el PDF: {str(e)}"
            }