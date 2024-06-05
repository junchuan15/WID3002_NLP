import React, { useState, useEffect } from 'react';
import './index.css';

const Chatbot = () => {
  const [dropdownOpen, setDropdownOpen] = React.useState(false);
  const welcomeMessage = { text: "Hello Freshies, Welcome to University Malaya! How can I help you?", user: false };
  const [messages, setMessages] = useState([welcomeMessage]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    try {
      // Add user's message to the state first
      setMessages(prevMessages => [...prevMessages, { text: input, user: true }]);

      const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const botMessages = data.map((msg) => ({ text: msg.text, user: false }));

      // Then add bot's response to the state
      setMessages(prevMessages => [...prevMessages, ...botMessages]);
      setInput('');
    } catch (error) {
      console.error('Error communicating with RASA:', error);
      setMessages(prevMessages => [...prevMessages, { text: "Error communicating with bot", user: false }]);
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  useEffect(() => {
    if (dropdownOpen) {
      const timer = setTimeout(() => setDropdownOpen(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [dropdownOpen]);

  return (
    <div className="chat-container">
      <div className="chat-header flex items-center gradient-bg">
        <img className="um-logo" src="/UM.png" alt="UM Logo" />
        <h1>FreshiesBot</h1>
        <div className="dropdown">
          <button className="dropbtn" onClick={() => setDropdownOpen(!dropdownOpen)}>
            <i className="fas fa-chevron-down"></i>
          </button>
        </div>
        <div className={`dropdown-content ${dropdownOpen ? 'show' : ''}`} id="dropdownContent">
          <p>FreshiesBot is a chatbot designed to assist new students in Universiti Malaya with their queries. Feel free to ask anything!</p>
        </div>
      </div>

      <div className="chat-history">
        {messages.map((msg, index) => (
          <div key={index} className={`message-container ${msg.user ? 'user-message-container' : 'bot-message-container'}`}>
            {!msg.user && (
              <div className="bot-profile">
                <img className="bot-profile-pic" src="technical-support.png" alt="Bot" />
                <div className="bot-label">FreshiesBot</div>
              </div>
            )}
            <div className={`message ${msg.user ? 'user-message' : 'bot-message'}`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="chat-input-container gradient-bg-bottom">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className={`chat-input ${input ? 'not-empty' : ''}`}
          placeholder="Enter your message"
        />
        <button className="chat-button sendBtn" onClick={handleSend}>
          <i className="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>

  );
};

export default Chatbot;
