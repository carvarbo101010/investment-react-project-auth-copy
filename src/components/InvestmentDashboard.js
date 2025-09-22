import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../App.css';

function InvestmentDashboard() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [ticker, setTicker] = useState('');
  const [debtToEquityData, setDebtToEquityData] = useState([]);

  const handleCalculateDebtToEquity = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/debt-to-equity', {
        ticker: ticker.toUpperCase()
      });

      setDebtToEquityData(response.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to calculate debt-to-equity ratio');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCSV = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios({
        method: 'POST',
        url: 'http://localhost:5000/api/debt-to-equity-csv',
        responseType: 'blob',
        data: {
          ticker: ticker.toUpperCase()
        }
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `debt_to_equity_${ticker.toUpperCase()}_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download CSV');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCashFlowCSV = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios({
        method: 'POST',
        url: 'http://localhost:5000/api/cash-flow-csv',
        responseType: 'blob',
        data: {
          ticker: ticker.toUpperCase()
        }
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cash_flow_${ticker.toUpperCase()}_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download cash flow CSV');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadEarningsGrowthCSV = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios({
        method: 'POST',
        url: 'http://localhost:5000/api/cash-earnings-growth-csv',
        responseType: 'blob',
        data: {
          ticker: ticker.toUpperCase()
        }
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Earnings_Growth_${ticker.toUpperCase()}_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download cash flow CSV');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadROECSV = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios({
        method: 'POST',
        url: 'http://localhost:5000/api/roe-csv',
        responseType: 'blob',
        data: {
          ticker: ticker.toUpperCase()
        }
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `ROE_${ticker.toUpperCase()}_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download cash flow CSV');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', marginBottom: '20px' }}>
          <h1>Key Metrics</h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span>Welcome, {user?.name || user?.email}</span>
            <button 
              onClick={handleLogout}
              style={{ 
                padding: '8px 16px', 
                backgroundColor: '#dc3545', 
                color: 'white', 
                border: 'none', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>
        </div>
        
        <div className="input-section">
          <label htmlFor="ticker">Stock Ticker Symbol:</label>
          <input
            id="ticker"
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g., AAPL, MSFT, GOOGL"
            disabled={loading}
          />
        </div>

        <div className="button-section">
          

          <button 
            onClick={handleDownloadCSV} 
            disabled={loading || !ticker.trim()}
            className="download-btn"
          >
            {loading ? 'Generating...' : 'Download Debt-to-Equity CSV'}
          </button>
        </div>

        <div className="input-section">
          <label htmlFor="ticker">Stock Ticker Symbol:</label>
          <input
            id="ticker"
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g., AAPL, MSFT, GOOGL"
            disabled={loading}
          />
        </div>

          <button 
            onClick={handleDownloadCashFlowCSV} 
            disabled={loading || !ticker.trim()}
            className="download-btn"
          >
            {loading ? 'Generating...' : 'Download Cash Flow CSV'}
          </button>
        
        <div className="input-section">
          <label htmlFor="ticker">Stock Ticker Symbol:</label>
          <input
            id="ticker"
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g., AAPL, MSFT, GOOGL"
            disabled={loading}
          />
        </div>

          <button 
            onClick={handleDownloadEarningsGrowthCSV} 
            disabled={loading || !ticker.trim()}
            className="download-btn"
          >
            {loading ? 'Generating...' : 'Download Cash Earnings Growth CSV'}
          </button>
        
        <div className="input-section">
          <label htmlFor="ticker">Stock Ticker Symbol:</label>
          <input
            id="ticker"
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g., AAPL, MSFT, GOOGL"
            disabled={loading}
          />
        </div>

          <button 
            onClick={handleDownloadROECSV} 
            disabled={loading || !ticker.trim()}
            className="download-btn"
          >
            {loading ? 'Generating...' : 'Download ROE CSV'}
          </button>

        {error && <p className="error">{error}</p>}

        {debtToEquityData.length > 0 && (
          <div className="results-section">
            <h2>Debt-to-Equity Ratios for {ticker.toUpperCase()}</h2>
            <table className="results-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Debt-to-Equity Ratio</th>
                </tr>
              </thead>
              <tbody>
                {debtToEquityData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.year}</td>
                    <td>{item.debt_to_equity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </header>
      
      <main className="App-body">
        <section className="bio-section">
          <div className="bio-container">
            <div className="bio-image">
              <img 
                src="/images/peter.jpg" 
                alt="Profile" 
                className="profile-photo"
              />
            </div>
            <div className="bio-text">
              <h2>Peter Lynch</h2>
              <p>
                Peter Lynch is a legendary American investor and former mutual fund manager, best known for managing the Fidelity Magellan Fund from 1977 to 1990. During his tenure, he achieved an extraordinary average annual return of 29.2%, making Magellan the best-performing mutual fund in the world and growing its assets from $18 million to $14 billion.
                
              </p>
              <p>
                In this project we have tried to use some principles from his book "One Up On Wall Street" in order to take better decisions while investing in stocks.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default InvestmentDashboard;