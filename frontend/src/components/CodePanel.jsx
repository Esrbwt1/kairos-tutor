import React from 'react';
import { Editor } from '@monaco-editor/react';
import './CodePanel.css';

const CodePanel = ({ code, setCode, handleRunCode, terminalOutput, isLoading }) => {
  
  const handleEditorChange = (value) => {
    setCode(value);
  };

  return (
    <div className="code-panel">
      <div className="editor-area">
        <Editor
          height="100%"
          width="100%"
          theme="vs-dark"
          language="rust"
          value={code} // Use 'value' instead of 'defaultValue' for controlled component
          onChange={handleEditorChange}
          options={{ fontSize: 14, minimap: { enabled: false } }}
        />
      </div>
      <div className="controls-area">
        <button onClick={handleRunCode} disabled={isLoading}>
          {isLoading ? 'Executing...' : 'Run Code'}
        </button>
      </div>
      <div className="terminal-area">
        <pre>{terminalOutput}</pre>
      </div>
    </div>
  );
};

export default CodePanel;