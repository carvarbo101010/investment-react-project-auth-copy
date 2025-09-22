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
  const [cashFlowData, setCashFlowData] = useState([]);
  const [earningsGrowthData, setEarningsGrowthData] = useState([]);
  const [roeData, setRoeData] = useState([]);

  const handleGetAllMetrics = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const tickerSymbol = ticker.toUpperCase();

      // Fetch all metrics in parallel
      const [debtToEquityRes, cashFlowRes, earningsGrowthRes, roeRes] = await Promise.all([
        axios.post('http://localhost:5000/api/debt-to-equity', { ticker: tickerSymbol }),
        axios.post('http://localhost:5000/api/cash-flow', { ticker: tickerSymbol }),
        axios.post('http://localhost:5000/api/earnings-growth', { ticker: tickerSymbol }),
        axios.post('http://localhost:5000/api/roe', { ticker: tickerSymbol })
      ]);

      setDebtToEquityData(debtToEquityRes.data.data);
      setCashFlowData(cashFlowRes.data.data);
      setEarningsGrowthData(earningsGrowthRes.data.data);
      setRoeData(roeRes.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch financial data');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    if (Math.abs(num) >= 1e9) {
      return `$${(num / 1e9).toFixed(2)}B`;
    } else if (Math.abs(num) >= 1e6) {
      return `$${(num / 1e6).toFixed(2)}M`;
    } else if (Math.abs(num) >= 1e3) {
      return `$${(num / 1e3).toFixed(2)}K`;
    }
    return `$${num.toFixed(2)}`;
  };

  const formatPercentage = (num) => {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    if (num === Infinity) return '∞%';
    if (num === -Infinity) return '-∞%';
    return `${num.toFixed(2)}%`;
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
            onKeyDown={(e) => e.key === 'Enter' && handleGetAllMetrics()}
          />
        </div>

        <div className="button-section">
          <button
            onClick={handleGetAllMetrics}
            disabled={loading || !ticker.trim()}
            className="primary-btn"
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              margin: '20px 0'
            }}
          >
            {loading ? 'Loading All Metrics...' : 'Get All Financial Metrics'}
          </button>
        </div>

        {error && <p className="error">{error}</p>}

        {((debtToEquityData && debtToEquityData.length > 0) || (cashFlowData && cashFlowData.length > 0) || (earningsGrowthData && earningsGrowthData.length > 0) || (roeData && roeData.length > 0)) && (
          <div className="results-container">
            <h2 style={{ textAlign: 'center', marginBottom: '30px' }}>Financial Analysis for {ticker.toUpperCase()}</h2>

            {debtToEquityData && debtToEquityData.length > 0 && (
              <div className="results-section">
                <h3>Debt-to-Equity Ratios</h3>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>Year</th>
                      <th>Debt-to-Equity Ratio</th>
                    </tr>
                  </thead>
                  <tbody>
                    {debtToEquityData && debtToEquityData.map((item, index) => (
                      <tr key={index}>
                        <td>{item.year}</td>
                        <td>{item.debt_to_equity}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {cashFlowData && cashFlowData.length > 0 && (
              <div className="results-section">
                <h3>Cash Flow Analysis</h3>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>Year</th>
                      <th>Operating CF</th>
                      <th>Investing CF</th>
                      <th>Financing CF</th>
                      <th>Free Cash Flow</th>
                      <th>FCF Calculation</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cashFlowData && cashFlowData.map((item, index) => (
                      <tr key={index}>
                        <td>{item.year}</td>
                        <td>{formatNumber(item.operating_cash_flow)}</td>
                        <td>{formatNumber(item.investing_cash_flow)}</td>
                        <td>{formatNumber(item.financing_cash_flow)}</td>
                        <td>{formatNumber(item.free_cash_flow)}</td>
                        <td>{item.fcf_calculation}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {earningsGrowthData && earningsGrowthData.length > 0 && (
              <div className="results-section">
                <h3>Earnings Growth</h3>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>Year</th>
                      <th>Net Income</th>
                      <th>Previous Year Income</th>
                      <th>Growth Rate</th>
                      <th>Growth Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {earningsGrowthData && earningsGrowthData.map((item, index) => (
                      <tr key={index}>
                        <td>{item.year}</td>
                        <td>{formatNumber(item.net_income)}</td>
                        <td>{formatNumber(item.previous_year_income)}</td>
                        <td style={{ color: item.growth_rate_percent >= 0 ? 'green' : 'red' }}>
                          {formatPercentage(item.growth_rate_percent)}
                        </td>
                        <td style={{ color: item.growth_amount >= 0 ? 'green' : 'red' }}>
                          {formatNumber(item.growth_amount)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {roeData && roeData.length > 0 && (
              <div className="results-section">
                <h3>Return on Equity (ROE)</h3>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>Year</th>
                      <th>Net Income</th>
                      <th>Total Equity</th>
                      <th>ROE %</th>
                    </tr>
                  </thead>
                  <tbody>
                    {roeData && roeData.map((item, index) => (
                      <tr key={index}>
                        <td>{item.year}</td>
                        <td>{formatNumber(item.net_income)}</td>
                        <td>{formatNumber(item.total_equity)}</td>
                        <td style={{ color: item.roe_percent >= 15 ? 'green' : item.roe_percent >= 10 ? 'orange' : 'red' }}>
                          {formatPercentage(item.roe_percent)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
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