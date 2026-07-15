import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isRegisterMode) {
        await api.post("/register", { name, email, password });
        setIsRegisterMode(false);
        setError("Registration successful! Please login.");
      } else {
        const res = await api.post("/login", { email, password });
        localStorage.setItem("token", res.data.access_token);
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2 className="page-title" style={{ textAlign: "center" }}>FinRelief AI 🚀</h2>
      <p className="page-subtitle" style={{ textAlign: "center" }}>
        {isRegisterMode ? "Create your account" : "Login to your account"}
      </p>

      {error && <p className="error-text">{error}</p>}

      <form onSubmit={handleSubmit}>
        {isRegisterMode && (
          <input
            className="form-input"
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        )}
        <input
          className="form-input"
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="form-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Please wait..." : isRegisterMode ? "Register" : "Login"}
        </button>
      </form>

      <span className="link-muted" onClick={() => setIsRegisterMode(!isRegisterMode)} style={{ cursor: "pointer" }}>
        {isRegisterMode ? "Already have an account? Login" : "New here? Create an account"}
      </span>
    </div>
  );
}
