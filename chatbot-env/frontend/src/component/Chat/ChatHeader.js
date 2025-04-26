import React from "react";
import PersonIcon from "../Icons/PersonIcon";
import "./ChatHeader.css";

export default function ChatHeader({ onProfileClick, onMenuClick }) {
  return (
    <div className="chat-header">
      <button className="profile-button" onClick={onProfileClick}>
        <PersonIcon small />
      </button>
      <h2 align="center">Student Information Chatbot</h2>
      <div className="menu-icon" onClick={onMenuClick}>☰</div>
    </div>
  );
}
