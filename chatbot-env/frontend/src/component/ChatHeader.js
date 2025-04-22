import React, { useState } from "react";
import axios from "axios";
import PersonIcon from "./PersonIcon";
import "./ChatHeader.css";

export default function ChatHeader() {
  const [showInfo, setShowInfo] = useState(false);
  const [info, setInfo] = useState(null);

  const handleToggle = async () => {
    if (!showInfo) {
      try {
        const userId = sessionStorage.getItem("user_id");
        const res = await axios.get(`http://127.0.0.1:8000/get_student_info/${userId}`);
        setInfo(res.data);
      } catch (err) {
        console.error("Error fetching student info", err);
        setInfo(null);
      }
    }
    setShowInfo(!showInfo);
  };

  return (
    <div className="chat-header">
      <button className="profile-button" onClick={handleToggle}>
        <PersonIcon small />
      </button>

      <h2>Student Chatbot</h2>

      <div className="menu-icon">☰</div>

      {showInfo && info && (
        <div className="profile-popup">
          <p><strong>Name:</strong> {info.name}</p>
          <p><strong>Email:</strong> {info.email}</p>
          <p><strong>GPA:</strong> {info.gpa}</p>
          <p><strong>Student ID:</strong> {info.id_number}</p>
          <p><strong>Emergency:</strong> {info.emergency_contact}</p>
          <p><strong>Address:</strong> {info.personal_address}</p>
        </div>
      )}
    </div>
  );
}
