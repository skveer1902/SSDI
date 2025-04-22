import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import ChatHeader from "./components/ChatHeader";
import ChatBody from "./components/ChatBody";
import ChatInput from "./components/ChatInput";

// Generate temporary session ID for user context
const generateSessionId = () => {
  return "session_" + Math.random().toString(36).substring(2, 10);
};

function App() {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you?", sender: "bot" },
  ]);

  const [sessionId] = useState(() => generateSessionId()); // constant per session
  const [userId, setUserId] = useState(() => sessionStorage.getItem("user_id") || "");
  const [userRole, setUserRole] = useState(() => sessionStorage.getItem("user_role") || "");

  const handleSend = async (text) => {
    const newMessages = [...messages, { text, sender: "user" }];
    setMessages(newMessages);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        user_id: sessionId, // we use a session-specific id to track chat session
        message: text,
      });

      let reply =
        res.data.response ||
        (res.data.results && JSON.stringify(res.data.results, null, 2)) ||
        "✅ Request sent.";

      // Detect and store user ID
      if (reply.includes("Successfully logged in as")) {
        const idMatch = reply.match(/ID\s(\w+)/i);
        if (idMatch) {
          const extractedId = idMatch[1];
          setUserId(extractedId);
          sessionStorage.setItem("user_id", extractedId);
        }

        const roleMatch = reply.match(/logged in as\s(\w+)/i);
        if (roleMatch) {
          const extractedRole = roleMatch[1].toLowerCase();
          setUserRole(extractedRole);
          sessionStorage.setItem("user_role", extractedRole);
        }
      }

      setMessages([...newMessages, { text: reply, sender: "bot" }]);
    } catch (error) {
      console.error("AxiosError:", error);
      setMessages([
        ...newMessages,
        { text: "❌ Backend error or CORS issue.", sender: "bot" },
      ]);
    }
  };

  return (
    <div className="mobile-container">
      <div className="chat-window">
        <ChatHeader />
        <ChatBody messages={messages} />
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}

export default App;