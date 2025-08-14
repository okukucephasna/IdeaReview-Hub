import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/login", {
        email,
        password
      });
      if (res.data.success) {
        setMessage("Login successful! Redirecting...");
        setTimeout(() => {
          navigate("/dashboard");
        }, 1000);
      } else {
        setMessage(res.data.message || "Login failed");
      }
    } catch (err) {
      setMessage("An error occurred. Please try again.");
    }
  };

  return (
    <>
      <Navbar />
      <div
        className="container vh-100 d-flex justify-content-center align-items-center bg-gradient"
        style={{
          background: "linear-gradient(to right, #fc5c7d, #6a82fb)",
          minHeight: "calc(100vh - 160px)" // prevents footer overlap
        }}
      >
        <div
          className="card shadow-lg p-4"
          style={{ maxWidth: "400px", width: "100%", borderRadius: "20px" }}
        >
          <h2 className="text-center mb-4 text-primary">Sign In</h2>
          {message && (
            <div
              className={`alert ${
                message.includes("successful") ? "alert-success" : "alert-danger"
              }`}
              role="alert"
            >
              {message}
            </div>
          )}
          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <label className="form-label fw-bold">Email address</label>
              <input
                type="email"
                className="form-control rounded-pill"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label fw-bold">Password</label>
              <input
                type="password"
                className="form-control rounded-pill"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
            </div>
            <button
              type="submit"
              className="btn btn-primary w-100 rounded-pill fw-bold"
            >
              Login
            </button>
          </form>
          <p className="text-center mt-3">
            Don’t have an account?{" "}
            <Link
              to="/signup"
              className="text-decoration-none fw-bold text-success"
            >
              Sign up here
            </Link>
          </p>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Login;
