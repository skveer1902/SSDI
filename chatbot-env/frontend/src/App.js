import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import ChatHeader from "./components/ChatHeader";
import ChatBody from "./components/ChatBody";
import ChatInput from "./components/ChatInput";
import LoginPage from "./components/LoginPage";

function App() {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you?", sender: "bot" },
  ]);

  // Read from sessionStorage
  const [userId, setUserId] = useState(() => sessionStorage.getItem("user_id") || "");
  const [userRole, setUserRole] = useState(() => sessionStorage.getItem("user_role") || "");

  const isLoggedIn = !!(userId && userRole);

  // Callback for when login succeeds
  const handleLogin = () => {
    setUserId(sessionStorage.getItem("user_id"));
    setUserRole(sessionStorage.getItem("user_role"));
  };

  const handleSend = async (text) => {
    const newMessages = [...messages, { text, sender: "user" }];
    setMessages(newMessages);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        user_id: userId, // ✅ Use actual logged-in ID here
        message: text,
      });

      let reply =
        res.data.response ||
        (res.data.results && JSON.stringify(res.data.results, null, 2)) ||
        "✅ Request sent.";

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
      {!isLoggedIn ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <div className="chat-window">
          <ChatHeader />
          <ChatBody messages={messages} />
          <ChatInput onSend={handleSend} />
        </div>
      )}
    </div>
  );
}

export default App;
