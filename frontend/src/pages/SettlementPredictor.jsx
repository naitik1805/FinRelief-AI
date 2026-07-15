import { useEffect, useState } from "react";
import api from "../services/api";

export default function SettlementPredictor() {
  const [settlements, setSettlements] = useState([]);
  const [strategy, setStrategy] = useState("");
  const [loadingStrategy, setLoadingStrategy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const fetchSettlements = async () => {
    try {
      const res = await api.get("/settlement-predictor");
      if (res.data.message) {
        setMessage(res.data.message);
      } else {
        setSettlements(res.data.settlements);
      }
    } catch (err) {
      setError("Failed to load settlement predictions");
    }
  };

  const fetchStrategy = async () => {
    setLoadingStrategy(true);
    try {
      const res = await api.get("/ai-negotiation-strategy");
      setStrategy(res.data.strategy);
    } catch (err) {
      setError("Failed to generate AI strategy");
    } finally {
      setLoadingStrategy(false);
    }
  };

  useEffect(() => {
    fetchSettlements();
  }, []);

  return (
    <div>
      <h1 className="page-title">Settlement Predictor</h1>
      <p className="page-subtitle">AI-driven settlement recommendations for each loan</p>

      {error && <p className="error-text">{error}</p>}
      {message && <p>{message}</p>}

      {settlements.map((s) => (
        <div className="card" key={s.loan_id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h3>{s.lender_name}</h3>
            <span className={`badge badge-${s.risk_category.toLowerCase()}`}>{s.risk_category} Risk</span>
          </div>
          <p style={{ marginTop: 10 }}>Outstanding Amount: ₹{s.outstanding_amount}</p>
          <p>Suggested Settlement: <b>{s.suggested_settlement_percentage}%</b> (₹{s.recommended_amount})</p>
          <p>Priority: {s.priority}</p>
        </div>
      ))}

      {settlements.length > 0 && (
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <h3>AI Negotiation Strategy</h3>
            <button className="btn-primary" style={{ width: "auto", padding: "8px 16px" }} onClick={fetchStrategy} disabled={loadingStrategy}>
              {loadingStrategy ? "Generating..." : "Generate Strategy"}
            </button>
          </div>
          {strategy && <pre style={{ whiteSpace: "pre-wrap", fontFamily: "var(--font-body)", fontSize: 14 }}>{strategy}</pre>}
        </div>
      )}
    </div>
  );
}
