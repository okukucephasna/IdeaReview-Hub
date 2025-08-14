// src/pages/Signup.jsx
import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function Signup() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      const res = await axios.post("http://localhost:5000/signup", formData);
      setMessage(res.data.message || "Signup successful!");
    } catch (err) {
      setMessage(err.response?.data?.error || "Signup failed!");
    }
  };

  return (
    <>
      <Navbar />
      <div
        className="container d-flex justify-content-center align-items-center"
        style={{ minHeight: "calc(100vh - 160px)" }}
      >
        <div
          className="card p-4 shadow-lg"
          style={{
            width: "100%",
            maxWidth: "400px",
            borderRadius: "15px",
            background: "white",
          }}
        >
          <h2 className="text-center mb-4 text-primary">Create Your Account</h2>
          {message && (
            <div
              className={`alert ${
                message.includes("successful") ? "alert-success" : "alert-danger"
              }`}
            >
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label fw-bold text-secondary">Email</label>
              <input
                type="email"
                name="email"
                className="form-control border-primary"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label fw-bold text-secondary">
                Password
              </label>
              <input
                type="password"
                name="password"
                className="form-control border-primary"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-100 fw-bold"
              style={{
                background: "linear-gradient(135deg, #667eea, #764ba2)",
                border: "none",
              }}
            >
              Sign Up
            </button>
          </form>

          <div className="mt-3 text-center">
            <span>Already have an account? </span>
            <Link
              to="/login"
              className="text-decoration-none fw-bold text-primary"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
