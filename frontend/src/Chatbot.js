import React, { useState } from 'react';
import './index.css';
import SendIcon from '@material-ui/icons/Send';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [showPlaceholder, setShowPlaceholder] = useState(true);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, user: true }]);
      setInput('');
      setShowPlaceholder(false);
      // Add bot response
      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, { text: "This is a bot response", user: false }]);
      }, 500);
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    if (e.target.value.trim() === '') {
      setShowPlaceholder(true); // Show the placeholder when input is empty
    } else {
      setShowPlaceholder(false); // Hide the placeholder when input is not empty
    }
  };

  return (
    <div className={`chat-container ${'bg-white text-black'}`}>
      <div className="chat-header flex items-center"> {/* Add flex container */}
        <h1 style={{ marginRight: '30px' }}>FreshiesBot</h1>
      </div>
      <div className={`chat-history ${'bg-gray-100'}`}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.user ? 'user-message' : 'bot-message'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className={`chat-input-container ${'bg-gray-100'}`}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className={`chat-input ${'bg-white text-black border-gray-300'}`}
          placeholder="Enter your message"
        />
        <button onClick={handleSend} className={`chat-button ${'bg-blue-500 text-white'}`} style={{ borderRadius: '15%', padding: '10px', marginLeft: '10px' }}>
          {/* <SendIcon /> */}
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
