import React from 'react';
import './SocraticTutorPanel.css';

const SocraticTutorPanel = () => {
  return (
    <div className="socratic-tutor-panel">
      <div className="messages-area">
        {/* Messages will be rendered here */}
        <div className="message assistant">
          Hello. I am Kairos. Present your code, and we will reason through it together.
        </div>
      </div>
      <div className="input-area">
        {/* A user input bar will eventually go here */}
        <input type="text" placeholder="This input is not yet functional." disabled />
      </div>
    </div>
  );
};

export default SocraticTutorPanel;