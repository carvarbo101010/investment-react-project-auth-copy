// src/components/Dashboard.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

// Dashboard component - protected page that users see after login
const Dashboard = () => {
  // Get user data and logout function from auth context
  const { user, logout } = useAuth();
  // Navigation hook for redirecting after logout
  const navigate = useNavigate();

  // Handle logout process
  const handleLogout = () => {
    // Call logout function from auth context
    logout();
    // Redirect to login page
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="dashboard-header-content">
          <h1 className="dashboard-title">Dashboard</h1>
          <div className="user-info">
            {/* Display user information */}
            <span className="user-name">Welcome, {user?.name || user?.email}</span>
            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <div className="welcome-section">
            <h2>Welcome to your Dashboard!</h2>
            <p>You have successfully logged in to the application.</p>
          </div>

          <div className="dashboard-cards">
            {/* Example dashboard cards */}
            <div className="dashboard-card">
              <h3>Profile</h3>
              <p>Manage your account settings and profile information.</p>
              <button className="card-button">View Profile</button>
            </div>

            <div className="dashboard-card">
              <h3>Analytics</h3>
              <p>View your usage statistics and analytics data.</p>
              <button className="card-button">View Analytics</button>
            </div>

            <div className="dashboard-card">
              <h3>Settings</h3>
              <p>Configure your application preferences and settings.</p>
              <button className="card-button">Open Settings</button>
            </div>
          </div>

          {/* Display user data for debugging */}
          <div className="user-debug-info">
            <h3>User Information:</h3>
            <pre>{JSON.stringify(user, null, 2)}</pre>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;