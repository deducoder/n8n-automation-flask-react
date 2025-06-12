import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [apiStatus, setApiStatus] = useState("Conectando...");

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

  return (
    <>
      <h1>{apiStatus}</h1>
    </>
  );
}

export default App;
