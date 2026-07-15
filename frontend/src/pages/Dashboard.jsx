import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [showLoanForm, setShowLoanForm] = useState(false);
  const [showProfileForm, setShowProfileForm] = useState(false);
  const [error, setError] = useState("");

  const [loanForm, setLoanForm] = useState({
    lender_name: "", loan_type: "", outstanding_amount: "",
    interest_rate: "", overdue_months: "", emi: ""
  });

  const [profileForm, setProfileForm] = useState({
    monthly_income: "", monthly_expenses: "", lump_sum_available: ""
  });

  const fetchDashboard = async () => {
    try {
      const res = await api.get("/dashboard-data");
      setData(res.data);
      setProfileForm({
        monthly_income: res.data.monthly_income,
        monthly_expenses: res.data.monthly_expenses,
        lump_sum_available: res.data.lump_sum_available
      });
    } catch (err) {
      setError("Failed to load dashboard data");
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleAddLoan = async (e) => {
    e.preventDefault();
    try {
      await api.post("/add-loan", {
        ...loanForm,
        outstanding_amount: parseFloat(loanForm.outstanding_amount),
        interest_rate: parseFloat(loanForm.interest_rate),
        overdue_months: parseInt(loanForm.overdue_months || 0),
        emi: parseFloat(loanForm.emi),
      });
      setShowLoanForm(false);
      setLoanForm({ lender_name: "", loan_type: "", outstanding_amount: "", interest_rate: "", overdue_months: "", emi: "" });
      fetchDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add loan");
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      await api.put("/update-profile", {
        monthly_income: parseFloat(profileForm.monthly_income),
        monthly_expenses: parseFloat(profileForm.monthly_expenses),
        lump_sum_available: parseFloat(profileForm.lump_sum_available || 0),
      });
      setShowProfileForm(false);
      fetchDashboard();
    } catch (err) {
      setError("Failed to update profile");
    }
  };

  const handleDeleteLoan = async (id) => {
    try {
      await api.delete(`/delete-loan/${id}`);
      fetchDashboard();
    } catch (err) {
      setError("Failed to delete loan");
    }
  };

  if (!data) return <p>Loading dashboard...</p>;

  const fh = data.financial_health;

  return (
    <div>
      <h1 className="page-title">Dashboard Overview</h1>
      <p className="page-subtitle">Your financial snapshot at a glance</p>

      {error && <p className="error-text">{error}</p>}

      <div className="card-grid">
        <div className="card">
          <div className="metric-label">Monthly Surplus</div>
          <div className="metric-value">₹{fh.surplus}</div>
        </div>
        <div className="card">
          <div className="metric-label">Total Outstanding</div>
          <div className="metric-value">₹{fh.total_outstanding}</div>
        </div>
        <div className="card">
          <div className="metric-label">Total EMI</div>
          <div className="metric-value">₹{fh.total_emi}</div>
        </div>
        <div className="card">
          <div className="metric-label">EMI Ratio</div>
          <div className="metric-value">{fh.emi_ratio_percent}%</div>
        </div>
        <div className="card">
          <div className="metric-label">Stress Level</div>
          <div className="metric-value">
            <span className={`badge badge-${fh.stress_level.toLowerCase()}`}>{fh.stress_level}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3>Financial Profile</h3>
          <button className="btn-primary" style={{ width: "auto", padding: "8px 16px" }} onClick={() => setShowProfileForm(!showProfileForm)}>
            {showProfileForm ? "Cancel" : "Edit Profile"}
          </button>
        </div>

        {!showProfileForm ? (
          <p>Monthly Income: ₹{data.monthly_income} &nbsp; | &nbsp; Monthly Expenses: ₹{data.monthly_expenses} &nbsp; | &nbsp; Lump Sum Available: ₹{data.lump_sum_available}</p>
        ) : (
          <form onSubmit={handleUpdateProfile}>
            <input className="form-input" type="number" placeholder="Monthly Income" value={profileForm.monthly_income}
              onChange={(e) => setProfileForm({ ...profileForm, monthly_income: e.target.value })} required />
            <input className="form-input" type="number" placeholder="Monthly Expenses" value={profileForm.monthly_expenses}
              onChange={(e) => setProfileForm({ ...profileForm, monthly_expenses: e.target.value })} required />
            <input className="form-input" type="number" placeholder="Lump Sum Available" value={profileForm.lump_sum_available}
              onChange={(e) => setProfileForm({ ...profileForm, lump_sum_available: e.target.value })} />
            <button className="btn-primary" type="submit">Save Profile</button>
          </form>
        )}
      </div>

      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3>Active Loans</h3>
          <button className="btn-primary" style={{ width: "auto", padding: "8px 16px" }} onClick={() => setShowLoanForm(!showLoanForm)}>
            {showLoanForm ? "Cancel" : "+ Add Loan"}
          </button>
        </div>

        {showLoanForm && (
          <form onSubmit={handleAddLoan} style={{ marginBottom: 20 }}>
            <input className="form-input" placeholder="Lender Name" value={loanForm.lender_name}
              onChange={(e) => setLoanForm({ ...loanForm, lender_name: e.target.value })} required />
            <input className="form-input" placeholder="Loan Type (e.g. EMI, Credit Card)" value={loanForm.loan_type}
              onChange={(e) => setLoanForm({ ...loanForm, loan_type: e.target.value })} required />
            <input className="form-input" type="number" placeholder="Outstanding Amount" value={loanForm.outstanding_amount}
              onChange={(e) => setLoanForm({ ...loanForm, outstanding_amount: e.target.value })} required />
            <input className="form-input" type="number" step="0.01" placeholder="Interest Rate (%)" value={loanForm.interest_rate}
              onChange={(e) => setLoanForm({ ...loanForm, interest_rate: e.target.value })} required />
            <input className="form-input" type="number" placeholder="Overdue Months" value={loanForm.overdue_months}
              onChange={(e) => setLoanForm({ ...loanForm, overdue_months: e.target.value })} />
            <input className="form-input" type="number" placeholder="Monthly EMI" value={loanForm.emi}
              onChange={(e) => setLoanForm({ ...loanForm, emi: e.target.value })} required />
            <button className="btn-primary" type="submit">Save Loan</button>
          </form>
        )}

        <table className="table">
          <thead>
            <tr>
              <th>Lender</th><th>Type</th><th>Outstanding</th><th>Interest</th><th>EMI</th><th>Overdue</th><th></th>
            </tr>
          </thead>
          <tbody>
            {data.loans.map((loan) => (
              <tr key={loan.id}>
                <td>{loan.lender_name}</td>
                <td>{loan.loan_type}</td>
                <td>₹{loan.outstanding_amount}</td>
                <td>{loan.interest_rate}%</td>
                <td>₹{loan.emi}</td>
                <td>{loan.overdue_months} mo</td>
                <td><button className="btn-danger" onClick={() => handleDeleteLoan(loan.id)}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
