import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import './Screen1.css';

const Screen1 = ({ onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileDrop = async (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onAnalysisComplete(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen1-container">
      <div
        className="drop-zone"
        onDrop={handleFileDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <img src="/track.png" alt="Track" className="track-bg" />
        <motion.img
          src="/car.png"
          alt="Car"
          className="car"
          animate={{
            x: loading ? [0, 500, 0] : 0,
          }}
          transition={{
            duration: 2,
            repeat: loading ? Infinity : 0,
            ease: "linear"
          }}
        />

        {!loading && (
          <div className="upload-area">
            <p>Drop your file here, or click to select a file</p>
            <input type="file" onChange={handleFileSelect} accept=".csv, .xls, .xlsx" />
            {error && <p className="error-message">{error}</p>}
          </div>
        )}
      </div>
    </div>
  );
};

export default Screen1;