import io
from docx import Document
from numpy import full

class DocumentExtractorService:
    @staticmethod
    def docx_extract(file):
        """
        Procesa un archivo DOCX usando python-docx para extraer el texto
        """
        try:
            file_bytes = io.BytesIO(file.read())
            document =  Document(file_bytes)
            full_text = []
            # Itera a trav[es de cada párrafo del documento Word
            for paragraph in document.paragraphs:
                if paragraph.text:
                    full_text.append(paragraph.text)   
            # Retorna los resultados de la extracción 
            return {
                "extracted_text": "\n".join(full_text),
                "message": "Texto extraido correctamente",
                "page_count": None,
                "status": "success"
            }
        except Exception as e:
            # Captura error inesperado
            print(f"Error inesperado al procesar DOCX: {e}")
            return {
                "extracted_text": None,
                "page_count": 0,
                "status": "error",
                "message": f"Ocurrió un error inesperado al procesar el DOCX: {str(e)}"
            }