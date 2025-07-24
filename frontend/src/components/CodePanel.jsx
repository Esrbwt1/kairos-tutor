import React, { useState } from 'react';
import { Editor } from '@monaco-editor/react';
import axios from 'axios';
import './CodePanel.css';

// The initial code that will appear in the editor
const initialCode = `fn main() {
println!("Hello from the Kairos code editor!");}`;

const CodePanel = () => {
  // State to hold the current code in the editor
  const [code, setCode] = useState(initialCode);
  // State to hold the output from the compiler/runner
  const [terminalOutput, setTerminalOutput] = useState('> Click "Run Code" to see the result.');
  // State to track if the code is currently being executed
  const [isLoading, setIsLoading] = useState(false);

  // This function is called when the content of the editor changes
  const handleEditorChange = (value) => {
    setCode(value);
  };

  // This function is called when the "Run Code" button is clicked
  const handleRunCode = async () => {
    setIsLoading(true);
    setTerminalOutput('> Executing...');
    try {
      // Make a POST request to our backend's /api/execute endpoint
      const response = await axios.post('http://127.0.0.1:8000/api/execute', {
        code: code,
      });
      
      // Update the terminal output with the result from the backend
      setTerminalOutput(response.data.output);
    } catch (error) {
      console.error("Error executing code:", error);
      setTerminalOutput(`Error: Failed to connect to the execution service.\n${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="code-panel">
      <div className="editor-area">
        {/* The Monaco Editor component */}
        <Editor
          height="100%"
          width="100%"
          theme="vs-dark"
          language="rust"
          defaultValue={initialCode}
          onChange={handleEditorChange}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
          }}
        />
      </div>
      <div className="controls-area">
        <button onClick={handleRunCode} disabled={isLoading}>
          {isLoading ? 'Executing...' : 'Run Code'}
        </button>
      </div>
      <div className="terminal-area">
        {/* The pre tag preserves whitespace and line breaks */}
        <pre>{terminalOutput}</pre>
      </div>
    </div>
  );
};

export default CodePanel;