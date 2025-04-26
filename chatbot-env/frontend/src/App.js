import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import ChatHeader from "./components/Chat/ChatHeader";
import ChatBody from "./components/Chat/ChatBody";
import ChatInput from "./components/Chat/ChatInput";
import LoginPage from "./components/Auth/LoginPage";
import ProfileCard from "./components/Panels/ProfileCard";
import MenuPanel from "./components/Panels/MenuPanel";
import HelpPanel from "./components/Panels/HelpPanel";

function App() {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you?", sender: "bot" },
  ]);
  
  const [userId, setUserId] = useState(() => sessionStorage.getItem("user_id") || "");
  const [userRole, setUserRole] = useState(() => sessionStorage.getItem("user_role") || "");
  const [showProfileCard, setShowProfileCard] = useState(false);
  const [showMenuPanel, setShowMenuPanel] = useState(false);
  const [showHelpPanel, setShowHelpPanel] = useState(false);

  const isLoggedIn = !!(userId && userRole);

  const handleLogin = () => {
    setUserId(sessionStorage.getItem("user_id"));
    setUserRole(sessionStorage.getItem("user_role"));
    setMessages([{ text: "Hi! How can I help you?", sender: "bot" }]);
  };

  const handleSend = async (text) => {
    const newMessages = [...messages, { text, sender: "user" }];
    setMessages(newMessages);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        user_id: userId,
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

  const handleLogout = async () => {
    try {
      if (userId) {
        await axios.post("http://127.0.0.1:8000/logout", { user_id: userId });
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
    sessionStorage.clear();
    setUserId("");
    setUserRole("");
    setMessages([{ text: "Hi! How can I help you?", sender: "bot" }]);
    setShowProfileCard(false);
    setShowMenuPanel(false);
    setShowHelpPanel(false);
  };

  return (
    <div className="mobile-container">
      {!isLoggedIn ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <>
          <div className="chat-window">
            <ChatHeader
              onProfileClick={() => setShowProfileCard(true)}
              onMenuClick={() => setShowMenuPanel(true)}
            />
            <ChatBody messages={messages} />
            <ChatInput onSend={handleSend} />
          </div>

          {showProfileCard && (
            <ProfileCard onClose={() => setShowProfileCard(false)} />
          )}

          {showMenuPanel && (
            <MenuPanel
              isOpen={true}
              onClose={() => setShowMenuPanel(false)}
              onHelp={() => {
                setShowMenuPanel(false);
                setShowHelpPanel(true);
              }}
              onLogout={handleLogout}
            />
          )}

          {showHelpPanel && (
            <HelpPanel
              isOpen={true}
              onClose={() => {
                setShowHelpPanel(false);
                setShowMenuPanel(true);
              }}
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
