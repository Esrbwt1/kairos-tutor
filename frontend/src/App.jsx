import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // State to store the message from the backend
  const [message, setMessage] = useState('Connecting to Kairos Backend...');

  // useEffect hook to fetch data when the component mounts
  useEffect(() => {
    // We define an async function inside the effect to use await
    const fetchData = async () => {
      try {
        // Make a GET request to our backend's root endpoint
        const response = await axios.get('http://127.0.0.1:8000/');
        // Update the state with the message from the response
        setMessage(response.data.message);
      } catch (error) {
        console.error("Error fetching data:", error);
        setMessage("Failed to connect to the backend.");
      }
    };

    fetchData();
  }, []); // The empty dependency array [] ensures this effect runs only once

  return (
    <>
      <h1>Project: Kairos</h1>
      <div className="card">
        <p>{message}</p>
      </div>
    </>
  );
}

export default App;