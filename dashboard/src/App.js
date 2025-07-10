import React, { useState, useEffect } from 'react';
import './App.css';
import LogViewer from './components/LogViewer';
import Header from './components/Header';

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        setLoading(true);
        // In production, replace with your actual API endpoint
        const response = await fetch('http://localhost:5000/logs');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setLogs(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch logs. Make sure the Game Agent is running.');
        console.error('Error fetching logs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
    // Poll for new logs every 5 seconds
    const interval = setInterval(fetchLogs, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <Header />
      <main className="container">
        <h2>Voice Command Logs</h2>
        {loading && <p>Loading logs...</p>}
        {error && <div className="error-message">{error}</div>}
        {!loading && !error && logs.length === 0 && (
          <p>No command logs found. Try speaking a command to your Game Agent.</p>
        )}
        {!loading && !error && logs.length > 0 && <LogViewer logs={logs} />}
      </main>
    </div>
  );
}

export default App;
