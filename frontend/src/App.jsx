import { useState, useEffect } from 'react';
import axios from 'axios';
import SocraticTutorPanel from './components/SocraticTutorPanel';
import CodePanel from './components/CodePanel';
import './App.css';

function App() {
  const [code, setCode] = useState('// Loading curriculum...');
  const [messages, setMessages] = useState([{ sender: 'assistant', text: 'Welcome to Kairos. Loading the first module...' }]);
  const [terminalOutput, setTerminalOutput] = useState('> Please wait.');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // This effect runs once on component mount to fetch the initial puzzle
    const fetchInitialModule = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/curriculum/initial');
        if (response.data.success) {
          const { module } = response.data;
          setCode(module.initialCode);
          setTerminalOutput(`> Module loaded: ${module.moduleName}. Press "Run Code" to begin.`);
          setMessages([{ sender: 'assistant', text: `Let's begin with a module on ${module.skillName}. The code on the right contains a common puzzle. Press "Run Code" to start our session.` }]);
        } else {
          // Handle error from backend
          setCode('// Error loading curriculum.');
          setMessages([{ sender: 'assistant', text: 'There was an error loading the curriculum. Please check the backend server.' }]);
        }
      } catch (error) {
        console.error("Error fetching initial module:", error);
        setCode('// Error: Could not connect to backend.');
        setMessages([{ sender: 'assistant', text: 'Fatal Error: Could not connect to the backend server.' }]);
      }
    };

    fetchInitialModule();
  }, []); // Empty array ensures this runs only once

  const handleCodeExecution = async () => {
    // ... (This function remains exactly the same as before)
    setIsLoading(true);
    setTerminalOutput('> Executing...');
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/execute', { code });
      const { output, socratic_message } = response.data;
      setTerminalOutput(output);
      
      if (socratic_message) {
        setMessages(prev => [...prev, { sender: 'assistant', text: socratic_message }]);
      }
    } catch (error) {
      console.error("Error executing code:", error);
      setTerminalOutput(`Error: Failed to connect to the execution service.\n${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <SocraticTutorPanel messages={messages} />
      <CodePanel 
        code={code}
        setCode={setCode}
        handleRunCode={handleCodeExecution}
        terminalOutput={terminalOutput}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;