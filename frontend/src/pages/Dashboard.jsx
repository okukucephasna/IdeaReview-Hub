// frontend/src/components/Dashboard.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard({ userEmail, setUserEmail }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    axios
      .post("http://localhost:5000/logout", {}, { withCredentials: true })
      .then(() => {
        setUserEmail("");
        navigate("/login");
      })
      .catch((err) => {
        console.error(err);
        alert("Logout failed. Please try again.");
      });
  };

  return (
    <div
      className="d-flex align-items-center justify-content-center vh-100"
      style={{
        background: "linear-gradient(135deg, #7b2ff7, #f107a3)",
      }}
    >
      <div
        className="card shadow-lg p-4"
        style={{ maxWidth: "500px", width: "100%", borderRadius: "20px" }}
      >
        <div className="text-center mb-4">
          <h2 className="fw-bold text-white">🎉 Welcome to Your Dashboard</h2>
          <p className="text-light">You are logged in as:</p>
          <h5 className="text-warning">{userEmail}</h5>
        </div>

        <div className="text-center">
          <button
            onClick={handleLogout}
            className="btn btn-danger px-4 py-2 fw-bold"
            style={{ borderRadius: "25px" }}
          >
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
