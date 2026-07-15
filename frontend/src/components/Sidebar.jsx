import { NavLink, useNavigate } from "react-router-dom";

export default function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const linkClass = ({ isActive }) =>
    isActive ? "sidebar-link active" : "sidebar-link";

  return (
    <div className="sidebar">
      <div className="sidebar-logo">FinRelief AI 🚀</div>
      <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
      <NavLink to="/financial-health" className={linkClass}>Financial Health</NavLink>
      <NavLink to="/settlement-predictor" className={linkClass}>Settlement Predictor</NavLink>
      <NavLink to="/negotiation-email" className={linkClass}>Negotiation Email</NavLink>
      <NavLink to="/know-your-rights" className={linkClass}>Know Your Rights</NavLink>
      <NavLink to="/history" className={linkClass}>History</NavLink>
      <div style={{ marginTop: "auto", paddingTop: 20 }}>
        <button className="btn-danger" style={{ width: "100%" }} onClick={handleLogout}>
          Log Out
        </button>
      </div>
    </div>
  );
}
