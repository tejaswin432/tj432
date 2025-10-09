import React from 'react';
import { saveAs } from 'file-saver';
import './Screen2.css';

const Screen2 = ({ results, onClose }) => {
  const { report, pieChart } = results;

  const handleDownloadReport = () => {
    // Convert JSON to CSV
    const headers = Object.keys(report[0]);
    const csvRows = [
      headers.join(','),
      ...report.map(row => headers.map(header => JSON.stringify(row[header])).join(','))
    ];
    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'report.csv');
  };

  const handleDownloadPieChart = () => {
    saveAs(pieChart, 'pie_chart.png');
  };

  const handleSendEmail = () => {
    // Placeholder for email functionality
    const email = document.getElementById('email-input').value;
    if (email) {
      console.log(`Sending report to ${email}`);
      // Here you would typically make another API call to a backend endpoint
      // that handles sending emails.
      alert(`Report will be sent to ${email}`);
    } else {
      alert('Please enter an email address.');
    }
  };

  return (
    <div className="screen2-container">
      <button className="close-button" onClick={onClose}>X</button>
      <div className="left-panel">
        <img src={pieChart} alt="Pie Chart" className="pie-chart" />
      </div>
      <div className="right-panel">
        <div className="action-item">
          <button onClick={handleDownloadReport}>Download Report</button>
        </div>
        <div className="action-item">
          <button onClick={handleDownloadPieChart}>Download Pie Chart</button>
        </div>
        <div className="action-item">
          <label htmlFor="email-input">Email Report</label>
          <input type="email" id="email-input" placeholder="Enter your email" />
          <button onClick={handleSendEmail}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Screen2;