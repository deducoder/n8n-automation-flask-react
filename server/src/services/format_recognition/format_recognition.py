import os
import mimetypes
import magic

class FormatRecognitionService:
    @staticmethod
    def format_recognition(file):
        """
        Identifica el tipo de arhivo basado en la extensión y contenido
        """
        # Identifica la exntensión
        filename = file.filename
        extension = os.path.splitext(filename)[1].lower() if filename else ""
        # Obtiene MIME basado en la extensión
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        # Lee el archivo para análisis del número de magic
        file_content = file.read()
        # Restablece el puntero al inicio
        file.seek(0)
        # Usa magic para detectar el tipo de archivo 
        content_type = magic.from_buffer(file_content, mime=True)
        # Determina la categoría 
        category = FormatRecognitionService._determinate_category(mime_type, content_type)
        return [
            "category", category,
            "content_type", content_type,
            "extension", extension,
            "mime_type", mime_type
        ]
        
    @staticmethod
    def _determinate_category(mime_type, content_type):
        """
        Determina la categoría general de archivo
        """
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type in ['application/pdf']:
            return 'document'
        elif mime_type in ['application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'application/vnd.ms-excel',
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return 'office_document'
        elif mime_type.startswith('text/'):
            return 'text'
        else:
            return 'other'