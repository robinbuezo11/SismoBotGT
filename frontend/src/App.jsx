import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [mensaje, setMensaje] = useState("");
  const [historial, setHistorial] = useState([]);

  const enviarMensaje = async () => {
    if (!mensaje.trim()) return;

    const nuevoMensaje = { remitente: "usuario", texto: mensaje };
    setHistorial([...historial, nuevoMensaje]);

    const res = await axios.post("http://localhost:8000/api/chat", { mensaje });
    const respuesta = { remitente: "chatbot", texto: res.data.respuesta };

    setHistorial([...historial, nuevoMensaje, respuesta]);
    setMensaje("");
  };

  return (
    <div className="App">
      <h2>Chatbot Informativo sobre Sismos en Guatemala</h2>
      <div className="chatbox">
        {historial.map((msg, i) => (
          <div key={i} className={`msg ${msg.remitente}`}>
            {msg.texto}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Escribe tu pregunta..."
          value={mensaje}
          onChange={(e) => setMensaje(e.target.value)}
        />
        <button onClick={enviarMensaje}>Enviar</button>
      </div>
    </div>
  );
}

export default App;