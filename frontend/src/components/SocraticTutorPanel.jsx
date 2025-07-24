import React, { useEffect, useRef } from 'react';
import './SocraticTutorPanel.css';

const SocraticTutorPanel = ({ messages }) => {
  const messagesEndRef = useRef(null);

  // This useEffect hook will automatically scroll to the bottom of the messages
  // whenever a new message is added.
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="socratic-tutor-panel">
      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {/* This empty div is the target for our auto-scrolling */}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input type="text" placeholder="Respond here... (not yet functional)" disabled />
      </div>
    </div>
  );
};

export default SocraticTutorPanel;