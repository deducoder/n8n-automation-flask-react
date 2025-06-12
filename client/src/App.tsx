import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [apiStatus, setApiStatus] = useState("Connecting...");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [isDragging, setIsDragging] = useState(false);

  // Consulta la salud de la API
  useEffect(() => {
    const fetchApiStatus = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/health`);
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          setApiStatus(data.message);
        } else {
          setApiStatus("API no disponible");
        }
      } catch (error) {
        setApiStatus("Error al conectar con la API");
      }
    };
    fetchApiStatus();
  }, []);

  // Selector de archivos
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  // Arrastre activo
  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  // Arrastre inactivo
  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
  };

  // Soltar archivo
  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus("");
    }
  };

  // Enviar archivo
  const handleSubmit = async () => {
    if (!selectedFile) {
      setUploadStatus("Por favor, selecciona un archivo");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploadStatus("Enviando archivo...");
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/file_upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const data = await response.json();
        setUploadStatus("Archivo enviado correctamente");
        setSelectedFile(null);
        console.log(data);
      } else {
        setUploadStatus("Error al enviar el archivo");
      }
    } catch (error) {
      setUploadStatus("Error al enviar el archivo");
    }
  };

  return (
    <div className="coontainer">
      <h1>API Status: {apiStatus}</h1>
      <div
        className={`upload-area ${isDragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          onChange={handleFileSelect}
          style={{ display: "none" }}
          id="file-input"
        ></input>
        <label htmlFor="file-input" className="upload-button">
          Elige un archivo
        </label>
        <p>O arrastra y suelta un archivo aquí</p>
        {selectedFile && (
          <div className="selected-file">
            <p>Selected file: {selectedFile.name}</p>
            <button onClick={handleSubmit}>Upload</button>
          </div>
        )}
        {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
      </div>
    </div>
  );
}

export default App;
