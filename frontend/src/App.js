import React, { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css'; 

function App() {
  const [loading, setLoading] = useState(false);
  const [biasedMetrics, setBiasedMetrics] = useState(null);
  const [mitigatedMetrics, setMitigatedMetrics] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null); // To track file upload

  // ✅ YOUR BACKEND URL
  const BACKEND_URL = "https://vigilant-memory-jjjw9q66grqwf56rj-8000.app.github.dev";

  // --- 1. HANDLE FILE UPLOAD ---
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadStatus(`✅ Uploaded! (${res.data.rows} rows)`);
      // Reset graphs when new data comes in
      setBiasedMetrics(null);
      setMitigatedMetrics(null);
    } catch (err) {
      console.error(err);
      setUploadStatus("❌ Upload Failed");
    }
    setLoading(false);
  };

  // --- 2. TRAIN BIASED MODEL ---
  const trainBiased = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/train/biased`, { n_samples: 3000 });
      setBiasedMetrics(res.data);
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend.");
    }
    setLoading(false);
  };

  // --- 3. TRAIN MITIGATED MODEL ---
  const trainMitigated = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/train/mitigated`, { n_samples: 3000 });
      setMitigatedMetrics(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const getChartData = (metrics) => [
    { name: 'Group A (e.g. Female)', rate: metrics.female_rate },
    { name: 'Group B (e.g. Male)', rate: metrics.male_rate }
  ];

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f5f7fa', minHeight: '100vh' }}>
      
      {/* HEADER */}
      <header style={{ marginBottom: '40px', textAlign: 'center' }}>
        <h1 style={{ color: '#2d3748' }}>🕵️‍♀️ The Algorithmic Auditor</h1>
        <p style={{ color: '#718096' }}>Upload your own data or use our synthetic dataset.</p>
        
        {/* FILE UPLOAD SECTION */}
        <div style={uploadBoxStyle}>
          <input type="file" onChange={handleFileUpload} accept=".csv" style={{marginBottom: '10px'}}/>
          <div style={{fontWeight: 'bold', color: uploadStatus?.includes('Failed') ? 'red' : 'green'}}>
            {uploadStatus || "No file uploaded (Using Synthetic Data)"}
          </div>
        </div>
      </header>

      {/* MAIN GRID */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '40px' }}>
        
        {/* --- LEFT: BIASED --- */}
        <div style={cardStyle}>
          <h2 style={{ color: '#e53e3e' }}>🔴 Phase 1: Biased Model</h2>
          <button onClick={trainBiased} disabled={loading} style={{...buttonStyle, backgroundColor: '#e53e3e'}}>
            {loading ? 'Processing...' : 'Train Standard Model'}
          </button>

          {biasedMetrics && (
            <div style={{ marginTop: '20px' }}>
              <div style={statGrid}>
                <StatBox label="Accuracy" value={(biasedMetrics.accuracy * 100).toFixed(1) + '%'} />
                <StatBox label="Bias Gap" value={biasedMetrics.bias_gap.toFixed(3)} color="#e53e3e" />
              </div>
              <div style={{ height: '300px', marginTop: '20px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={getChartData(biasedMetrics)}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false}/>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#e53e3e" name="Approval Rate" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>

        {/* --- RIGHT: MITIGATED --- */}
        <div style={cardStyle}>
          <h2 style={{ color: '#38a169' }}>🟢 Phase 2: Ethical Model</h2>
          <button onClick={trainMitigated} disabled={!biasedMetrics || loading} style={{...buttonStyle, backgroundColor: '#38a169', opacity: !biasedMetrics ? 0.5 : 1}}>
            {loading ? 'Processing...' : 'Apply Bias Mitigation'}
          </button>

          {mitigatedMetrics && (
            <div style={{ marginTop: '20px' }}>
              <div style={statGrid}>
                <StatBox label="Accuracy" value={(mitigatedMetrics.accuracy * 100).toFixed(1) + '%'} />
                <StatBox label="Bias Gap" value={mitigatedMetrics.bias_gap.toFixed(3)} color="#38a169" />
              </div>
              <div style={{ height: '300px', marginTop: '20px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={getChartData(mitigatedMetrics)}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#38a169" name="Approval Rate" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

// --- STYLES ---
const cardStyle = { backgroundColor: 'white', padding: '30px', borderRadius: '16px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' };
const uploadBoxStyle = { backgroundColor: 'white', padding: '20px', borderRadius: '10px', display: 'inline-block', marginTop: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' };
const buttonStyle = { color: 'white', border: 'none', padding: '12px 20px', borderRadius: '8px', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold', width: '100%', marginTop: '10px' };
const statGrid = { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' };
const StatBox = ({ label, value, color }) => (
  <div style={{ textAlign: 'center', padding: '15px', backgroundColor: '#edf2f7', borderRadius: '12px' }}>
    <div style={{ fontSize: '12px', color: '#718096' }}>{label}</div>
    <div style={{ fontSize: '24px', fontWeight: 'bold', color: color }}>{value}</div>
  </div>
);

export default App;