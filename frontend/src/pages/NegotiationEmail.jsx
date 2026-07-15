import { useEffect, useState } from "react";
import api from "../services/api";

export default function NegotiationEmail() {
  const [loans, setLoans] = useState([]);
  const [selectedLoan, setSelectedLoan] = useState("");
  const [emailContent, setEmailContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const fetchLoans = async () => {
    try {
      const res = await api.get("/loans");
      setLoans(res.data);
      if (res.data.length > 0) setSelectedLoan(res.data[0].id);
    } catch (err) {
      setError("Failed to load loans");
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  const handleGenerate = async () => {
    if (!selectedLoan) return;
    setLoading(true);
    setError("");
    try {
      const res = await api.get(`/generate-negotiation-email/${selectedLoan}`);
      setEmailContent(res.data.email);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate negotiation email");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(emailContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      <h1 className="page-title">Negotiation Email Generator</h1>
      <p className="page-subtitle">Generate lender-specific settlement request letters</p>

      {error && <p className="error-text">{error}</p>}

      <div className="card">
        <label style={{ fontSize: 13, color: "var(--text-secondary)" }}>Select Loan Account</label>
        <select
          className="form-input"
          value={selectedLoan}
          onChange={(e) => setSelectedLoan(e.target.value)}
        >
          {loans.map((loan) => (
            <option key={loan.id} value={loan.id}>
              {loan.lender_name} — ₹{loan.outstanding_amount}
            </option>
          ))}
        </select>
        <button className="btn-primary" onClick={handleGenerate} disabled={loading || !selectedLoan}>
          {loading ? "Generating..." : "Generate Letter"}
        </button>
      </div>

      {emailContent && (
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <h3>Generated Letter</h3>
            <button className="btn-primary" style={{ width: "auto", padding: "6px 14px" }} onClick={handleCopy}>
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>
          <pre style={{ whiteSpace: "pre-wrap", fontFamily: "var(--font-body)", fontSize: 14, lineHeight: 1.6 }}>
            {emailContent}
          </pre>
        </div>
      )}
    </div>
  );
}
