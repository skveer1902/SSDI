import React from "react";
import "./HelpPanel.css";

export default function HelpPanel({ isOpen, onClose }) {
  return (
    <div className={`help-slide-panel ${isOpen ? "open" : "closed"}`}>
      <div className="help-content">
        <button className="close-button" onClick={onClose}>✖</button>
        <div className="help-heading">Emergency Contacts</div>
        <div className="help-section">
          <div className="help-option"><strong>Campus Police:</strong> 123-456-7890</div>
          <div className="help-option"><strong>Medical Emergency:</strong> 987-654-3210</div>
        </div>
        <div className="help-heading">Helpful Prompts</div>
        <div className="help-section">
            <div className="help-option">What is my GPA?</div>
            <div className="help-option">What’s my tuition fee?</div>
            <div className="help-option">Show my personal details</div>
            <div className="help-option">What’s my emergency contact?</div>
            <div className="help-option">When does the semester start?</div>
            <div className="help-option">Show me my ID card info</div>
            <div className="help-option">What is my tuition status?</div>
            <div className="help-option">List available job postings</div>
            <div className="help-option">Show me the academic calendar</div>
            <div className="help-option">How do I contact campus police?</div>
        </div>

      </div>
    </div>
  );
}
