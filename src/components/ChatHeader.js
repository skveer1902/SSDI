import React from 'react';
import PersonIcon from './PersonIcon';

export default function ChatHeader() {
  return (
    <div className="chat-header">
      <PersonIcon small />
      <h2>Student Information Chatbot</h2>
      <div className="menu-icon">☰</div>
    </div>
  );
}
