import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const API_URL = 'http://localhost:8000/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      setIsAuthenticated(true);
      fetchDatasets();
    }
  }, [token]);


  const handleAuth = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegister ? '/auth/register/' : '/auth/login/';
      const data = isRegister ? { username, password, email } : { username, password };

      console.log('Sending request to:', `${API_URL}${endpoint}`);
      console.log('Data:', data);

      const response = await axios.post(`${API_URL}${endpoint}`, data);

      console.log('Response:', response.data);

      const newToken = response.data.token;

      if (!newToken) {
        throw new Error('No token received');
      }

      setToken(newToken);
      localStorage.setItem('token', newToken);
      setIsAuthenticated(true);
      setUsername('');
      setPassword('');
      setEmail('');
    } catch (err) {
      console.error('Auth error:', err);
      console.error('Error response:', err.response?.data);
      setError(err.response?.data?.error || err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setDatasets([]);
    setSelectedDataset(null);
  };

  const fetchDatasets = async () => {
    try {
      const response = await axios.get(`${API_URL}/datasets/`, {
        headers: { Authorization: `Token ${token}` }
      });
      setDatasets(response.data);
    } catch (err) {
      setError('Failed to fetch datasets');
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/datasets/upload/`, formData, {
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setSelectedDataset(response.data);
      fetchDatasets();
      setFile(null);
      document.getElementById('fileInput').value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetClick = async (datasetId) => {
    try {
      const response = await axios.get(`${API_URL}/datasets/${datasetId}/summary/`, {
        headers: { Authorization: `Token ${token}` }
      });
      setSelectedDataset(response.data);
    } catch (err) {
      setError('Failed to fetch dataset details');
    }
  };

  const handleDownloadPDF = async (datasetId) => {
    try {
      const response = await axios.get(`${API_URL}/datasets/${datasetId}/generate_pdf/`, {
        headers: { Authorization: `Token ${token}` },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download PDF');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h1>Chemical Equipment Visualizer</h1>
          <h2>{isRegister ? 'Register' : 'Login'}</h2>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleAuth}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            {isRegister && (
              <input
                type="email"
                placeholder="Email (optional)"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            )}
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Processing...' : (isRegister ? 'Register' : 'Login')}
            </button>
          </form>

          <p className="auth-toggle">
            {isRegister ? 'Already have an account? ' : "Don't have an account? "}
            <span onClick={() => setIsRegister(!isRegister)}>
              {isRegister ? 'Login' : 'Register'}
            </span>
          </p>
        </div>
      </div>
    );
  }

  const getAveragesChartData = () => {
    if (!selectedDataset) return null;

    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [{
        label: 'Average Values',
        data: [
          selectedDataset.avg_flowrate?.toFixed(2),
          selectedDataset.avg_pressure?.toFixed(2),
          selectedDataset.avg_temperature?.toFixed(2)
        ],
        backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
      }]
    };
  };

  const getTypeDistributionData = () => {
    if (!selectedDataset?.type_distribution) return null;

    const types = Object.keys(selectedDataset.type_distribution);
    const counts = Object.values(selectedDataset.type_distribution);

    return {
      labels: types,
      datasets: [{
        label: 'Equipment Count',
        data: counts,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ],
      }]
    };
  };

  return (
    <div className="app">
      <header>
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>

      <div className="main-container">
        <div className="sidebar">
          <div className="upload-section">
            <h3>Upload CSV</h3>
            {error && <div className="error">{error}</div>}
            <form onSubmit={handleUpload}>
              <input
                id="fileInput"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
              />
              <button type="submit" disabled={loading || !file}>
                {loading ? 'Uploading...' : 'Upload'}
              </button>
            </form>
          </div>

          <div className="history-section">
            <h3>Recent Datasets (Last 5)</h3>
            {datasets.length === 0 ? (
              <p className="no-data">No datasets uploaded yet</p>
            ) : (
              <ul className="dataset-list">
                {datasets.map(ds => (
                  <li
                    key={ds.id}
                    onClick={() => handleDatasetClick(ds.id)}
                    className={selectedDataset?.id === ds.id ? 'active' : ''}
                  >
                    <div className="dataset-name">{ds.filename}</div>
                    <div className="dataset-date">
                      {new Date(ds.uploaded_at).toLocaleString()}
                    </div>
                    <div className="dataset-count">{ds.total_records} records</div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="content">
          {!selectedDataset ? (
            <div className="placeholder">
              <h2>Welcome!</h2>
              <p>Upload a CSV file or select a dataset from history to view visualizations</p>
            </div>
          ) : (
            <>
              <div className="dataset-header">
                <h2>{selectedDataset.filename}</h2>
                <button
                  onClick={() => handleDownloadPDF(selectedDataset.id)}
                  className="pdf-btn"
                >
                  Download PDF Report
                </button>
              </div>

              <div className="stats-grid">
                <div className="stat-card">
                  <h4>Total Records</h4>
                  <p className="stat-value">{selectedDataset.total_records}</p>
                </div>
                <div className="stat-card">
                  <h4>Avg Flowrate</h4>
                  <p className="stat-value">{selectedDataset.avg_flowrate?.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h4>Avg Pressure</h4>
                  <p className="stat-value">{selectedDataset.avg_pressure?.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h4>Avg Temperature</h4>
                  <p className="stat-value">{selectedDataset.avg_temperature?.toFixed(2)}</p>
                </div>
              </div>

              <div className="charts-container">
                <div className="chart-box">
                  <h3>Average Parameter Values</h3>
                  {getAveragesChartData() && (
                    <Bar data={getAveragesChartData()} options={{ responsive: true, maintainAspectRatio: false }} />
                  )}
                </div>
                <div className="chart-box">
                  <h3>Equipment Type Distribution</h3>
                  {getTypeDistributionData() && (
                    <Pie data={getTypeDistributionData()} options={{ responsive: true, maintainAspectRatio: false }} />
                  )}
                </div>
              </div>

              <div className="table-container">
                <h3>Equipment Details</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Equipment Name</th>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedDataset.equipment?.map(eq => (
                      <tr key={eq.id}>
                        <td>{eq.equipment_name}</td>
                        <td>{eq.equipment_type}</td>
                        <td>{eq.flowrate.toFixed(2)}</td>
                        <td>{eq.pressure.toFixed(2)}</td>
                        <td>{eq.temperature.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;