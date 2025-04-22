import React from 'react';

export default function ChatBody({ messages }) {
  return (
    <div className="chat-body">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.sender}`}>
          {msg.text}
        </div>
      ))}
    </div>
  );
}
