// ✅ LoginPage.js
import React, { useState } from "react";
import axios from "axios";
import "./LoginPage.css";

function LoginPage({ onLogin }) {
  const [role, setRole] = useState("student");
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/login", {
        role,
        user_id: userId,
        password,
      });

      if (res.data.status === "success") {
        sessionStorage.setItem("user_id", res.data.user_id);
        sessionStorage.setItem("user_role", res.data.role);
        onLogin();
      }
    } catch (error) {
      console.error(error);
      setError("Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="login-wrapper">
      <form className="login-box" onSubmit={handleLogin}>
        <h2>Login to Chatbot</h2>

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

        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        <button type="submit">Login</button>

        {error && <div className="error-message">{error}</div>}
      </form>
    </div>
  );
}

export default LoginPage;
