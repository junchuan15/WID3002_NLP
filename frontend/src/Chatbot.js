import React, { useState, useEffect, useRef } from 'react';
import './index.css';
import useTypingEffect from './useTypingEffect';

const Chatbot = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false); 
  const welcomeMessage = { text: "Hello Freshies, Welcome to Universiti Malaya! How can I help you?", user: false, id: 0 };
  const [messages, setMessages] = useState([welcomeMessage]);
  const [input, setInput] = useState('');
  const chatHistoryRef = useRef(null);
  
  const handleSend = async () => {
    try {
      setMessages(prevMessages => [...prevMessages, { text: input, user: true, id: prevMessages.length }]);
  
      setTimeout(async () => {
        try {
          const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: input }),
          });
  
          const data = await response.json();
          const botMessages = data.map((msg, index) => ({ text: msg.text, user: false, id: messages.length + index + 1 }));
  
          setMessages(prevMessages => [...prevMessages, ...botMessages]);
          setInput('');
        } catch (error) {
          console.error('Error communicating with RASA:', error);
          setMessages(prevMessages => [...prevMessages, { text: "Error communicating with bot", user: false, id: prevMessages.length }]);
        }
      }, 2000); 
    } catch (error) {
      console.error('Error:', error);
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

  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="chat-header flex items-center gradient-bg">
        <img className="um-logo" src="/UM.png" alt="UM Logo" />
        <h1 className="freshies-bot-title">
          <span className="freshies">Freshies</span>
          <span className="bot">Bot</span>
          </h1>        
        <div className="dropdown">
          <button className="dropbtn" onClick={() => setDropdownOpen(!dropdownOpen)}>
            <i className="fas fa-chevron-down"></i>
          </button>
        </div>
        <div className={`dropdown-content ${dropdownOpen ? 'show' : ''}`} id="dropdownContent">
          <p>FreshiesBot is a chatbot designed to assist new students in Universiti Malaya with their queries. Feel free to ask anything!</p>
        </div>
      </div>

      <div className="chat-history" ref={chatHistoryRef}>
        {messages.map((msg, index) => (
          <Message key={index} msg={msg} />
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

const Message = ({ msg }) => {
  const botMessage = !msg.user;
  const text = useTypingEffect(msg.text);

  return (
    <div className={`message-container ${msg.user ? 'user-message-container' : 'bot-message-container'}`}>
      {!msg.user && (
        <div className="bot-profile">
          <img className="bot-profile-pic" src="technical-support.png" alt="Bot" />
          <div className="bot-label"></div>
        </div>
      )}
      <div className={`message ${msg.user ? 'user-message' : 'bot-message'}`}>
        {botMessage ? text : msg.text}
      </div>
    </div>
  );
};


export default Chatbot;
