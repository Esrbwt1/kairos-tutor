import { useState } from 'react';
import axios from 'axios';
import SocraticTutorPanel from './components/SocraticTutorPanel';
import CodePanel from './components/CodePanel';
import './App.css';

// The initial code that will be our first puzzle for the user
const initialCode = `fn main() {
let s1 = String::from("hello");
let s2 = s1;
println!("{}, world!", s1); }`;

const initialMessages = [
  { sender: 'assistant', text: 'Hello. Welcome to Kairos. The code on the right contains a common Rust error. Press "Run Code" to begin our session.' }
];

function App() {
  const [code, setCode] = useState(initialCode);
  const [terminalOutput, setTerminalOutput] = useState('> Press "Run Code" to compile.');
  const [messages, setMessages] = useState(initialMessages);
  const [isLoading, setIsLoading] = useState(false);

  const handleCodeExecution = async () => {
    setIsLoading(true);
    setTerminalOutput('> Executing...');
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/execute', { code });
      const { output, socratic_message } = response.data;

      setTerminalOutput(output);
      
      if (socratic_message) {
        // If the backend AI has a message, add it to our chat
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