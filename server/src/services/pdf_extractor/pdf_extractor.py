import io
import pdfplumber

class PDFExtractorService:
    @staticmethod
    def pdf_extract(file):
        """
        Procesa un archivo PDF usando pdfplumber para extraer el texto
        """
        try: 
            # Convierte el File a un objeto BytesIO
            file_bytes = io.BytesIO(file.read())
            full_text = []
            page_count = 0
            # Abre el PDF con pdfplumber
            with pdfplumber.open(file_bytes) as pdf:
                # Itera a través de cada página del PDF
                for page in pdf.pages:
                    # Extrae el texto de cada página
                    page_text = page.extract_text()
                    if page_text:
                        full_text.append(page_text)
                        page_count += 1
            # Retorna los resultados de la extracción
            return {
                "extracted_text": "\n".join(full_text),
                "message": "Texto extraído correctamente",
                "page_count": page_count,
                "status": "success"
            }
        except Exception as e:
            # Captura error inesperado
            print(f"Error inesperado al procesar PDF: {e}")
            return {
                "extracted_text": None,
                "page_count": 0,
                "status": "error",
                "message": f"Ocurrió un error inesperado al procesar el PDF: {str(e)}"
            }