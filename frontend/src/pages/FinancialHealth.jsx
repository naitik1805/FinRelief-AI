import { useEffect, useState } from "react";
import api from "../services/api";

export default function FinancialHealth() {
  const [health, setHealth] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [extraPayment, setExtraPayment] = useState(0);
  const [error, setError] = useState("");

  const fetchHealth = async () => {
    try {
      const res = await api.get("/financial-health");
      setHealth(res.data);
    } catch (err) {
      setError("Failed to load financial health data");
    }
  };

  const fetchTimeline = async () => {
    try {
      const res = await api.get(`/debt-timeline?extra_payment=${extraPayment || 0}`);
      setTimeline(res.data);
    } catch (err) {
      setError("Failed to load debt timeline");
    }
  };

  useEffect(() => {
    fetchHealth();
    fetchTimeline();
  }, []);

  if (!health) return <p>Loading financial health...</p>;

  return (
    <div>
      <h1 className="page-title">Financial Health</h1>
      <p className="page-subtitle">Overall debt stress and repayment overview</p>

      {error && <p className="error-text">{error}</p>}

      <div className="card-grid">
        <div className="card">
          <div className="metric-label">Monthly Surplus</div>
          <div className="metric-value">₹{health.surplus}</div>
        </div>
        <div className="card">
          <div className="metric-label">Debt-to-Income</div>
          <div className="metric-value">{health.debt_to_income_percent}%</div>
        </div>
        <div className="card">
          <div className="metric-label">Total Loans</div>
          <div className="metric-value">{health.total_loans}</div>
        </div>
        <div className="card">
          <div className="metric-label">Stress Level</div>
          <div className="metric-value">
            <span className={`badge badge-${health.stress_level.toLowerCase()}`}>{health.stress_level}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 12 }}>Debt Repayment Timeline Simulation</h3>
        <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
          <input
            className="form-input"
            type="number"
            placeholder="Extra Monthly Payment (optional)"
            value={extraPayment}
            onChange={(e) => setExtraPayment(e.target.value)}
            style={{ marginBottom: 0 }}
          />
          <button className="btn-primary" style={{ width: "auto", padding: "0 20px" }} onClick={fetchTimeline}>
            Simulate
          </button>
        </div>

        {timeline && timeline.message && <p>{timeline.message}</p>}

        {timeline && !timeline.message && (
          <>
            <p>Estimated months to become debt-free: <b>{timeline.months_to_debt_free}</b></p>
            <table className="table" style={{ marginTop: 12 }}>
              <thead><tr><th>Month</th><th>Remaining Balance</th></tr></thead>
              <tbody>
                {timeline.timeline_preview.map((t) => (
                  <tr key={t.month}><td>{t.month}</td><td>₹{t.remaining_balance}</td></tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}
