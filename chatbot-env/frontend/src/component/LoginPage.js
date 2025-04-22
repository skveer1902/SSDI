// src/components/LoginPage.js
import React, { useState } from "react";
import axios from "axios";
import "./LoginPage.css";

export default function LoginPage({ onLogin }) {
  const [role, setRole] = useState("student");
  const [userId, setUserId] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/login", {
        role,
        user_id: userId,
      });

      if (response.data.status === "success") {
        sessionStorage.setItem("user_id", userId);
        sessionStorage.setItem("user_role", role);
        onLogin(); // triggers transition to chat
      } else {
        setError(response.data.message || "Login failed.");
      }
    } catch (err) {
      console.error(err);
      setError("Server error. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <h2>Login to Chatbot</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <label>
          Role:
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="student">Student</option>
            <option value="faculty">Faculty</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        <label>
          User ID:
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
          />
        </label>

        {/* <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label> */}

        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
