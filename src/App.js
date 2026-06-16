import React, { useEffect, useState } from "react";
import axios from "axios";
import VideoPlayer from "./components/VideoPlayer";
import Joystick from "./components/Joystick";
import LogPanel from "./components/LogPanel";

const API_BASE = "http://localhost:8000/api";

function App() {
  const [logs, setLogs] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("disconnected");

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/control/");

    ws.onopen = () => setConnectionStatus("connected");
    ws.onclose = () => setConnectionStatus("disconnected");
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setLogs((prev) => [JSON.stringify(message), ...prev].slice(0, 20));
    };

    return () => ws.close();
  }, []);

  const sendControl = async (action) => {
    setLogs((prev) => [`sending: ${action}`, ...prev].slice(0, 20));
    try {
      const response = await axios.post(`${API_BASE}/control/`, new URLSearchParams({ action }));
      setLogs((prev) => [`response: ${JSON.stringify(response.data)}`, ...prev].slice(0, 20));
    } catch (error) {
      setLogs((prev) => [`error: ${error.message}`, ...prev].slice(0, 20));
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4">
      <header className="mb-6">
        <h1 className="text-3xl font-bold">Autonomous Surveillance Rover</h1>
        <p className="text-slate-400">Edge AI + Django backend monitoring live ESP32-CAM feed</p>
      </header>

      <main className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <section className="rounded-3xl bg-slate-900 p-5 shadow-xl">
          <VideoPlayer />
        </section>

        <section className="space-y-6">
          <Joystick onControl={sendControl} />
          <LogPanel logs={logs} connectionStatus={connectionStatus} />
        </section>
      </main>
    </div>
  );
}

export default App;
