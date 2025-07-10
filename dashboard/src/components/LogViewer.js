import React from 'react';
import './LogViewer.css';

function LogViewer({ logs }) {
  return (
    <div className="log-viewer">
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Command</th>
            <th>Transcript</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, index) => (
            <tr key={index}>
              <td>{log.timestamp}</td>
              <td>{log.command}</td>
              <td>{log.transcript}</td>
              <td>{log.result}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LogViewer;
