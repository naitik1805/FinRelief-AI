import { useEffect, useState } from "react";
import api from "../services/api";

export default function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get("/ai-history");
        setHistory(res.data);
      } catch (err) {
        setError("Failed to load AI history");
      }
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h1 className="page-title">AI Interaction History</h1>
      <p className="page-subtitle">Review your past AI-generated strategies and letters</p>

      {error && <p className="error-text">{error}</p>}

      {history.length === 0 && <p>No AI interactions yet. Generate a strategy or negotiation email to see it here.</p>}

      {history.map((h) => (
        <div className="card" key={h.id}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
            <b>{h.query_type}</b>
            <span style={{ fontSize: 12, color: "var(--text-secondary)" }}>
              {new Date(h.generated_at).toLocaleString()}
            </span>
          </div>
          <pre style={{ whiteSpace: "pre-wrap", fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-secondary)" }}>
            {h.response.length > 400 ? h.response.slice(0, 400) + "..." : h.response}
          </pre>
        </div>
      ))}
    </div>
  );
}
