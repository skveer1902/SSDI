import React, { useState } from "react";
import "./LoginPage.css"; // create for styling
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [role, setRole] = useState("student");
  const [userId, setUserId] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!userId) {
      alert("Please enter your User ID");
      return;
    }

    // Save to session storage
    sessionStorage.setItem("user_id", userId);
    sessionStorage.setItem("user_role", role);

    // Navigate to chatbot
    navigate("/chat");
  };

  return (
    <div className="login-container">
      <h2>Student Information Chatbot</h2>
      <form className="login-form" onSubmit={handleLogin}>
        <label>Role</label>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="student">Student</option>
          <option value="faculty">Faculty</option>
          <option value="admin">Admin</option>
        </select>

        <label>User ID</label>
        <input
          type="text"
          placeholder="Enter your ID (e.g., ID0001)"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />

        {/* <label>Password</label>
        <input type="password" placeholder="(Coming soon)" disabled /> */}

        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
