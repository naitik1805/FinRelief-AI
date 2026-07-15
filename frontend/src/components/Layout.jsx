import { Navigate, Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

export default function Layout() {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
}
