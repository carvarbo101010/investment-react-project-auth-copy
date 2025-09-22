// src/components/Login.js
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Navigate } from 'react-router-dom';
import './Login.css'; // We'll create this CSS file next

const Login = () => {
  // Get auth functions from context
  const { login, isAuthenticated } = useAuth();
  // Hook for programmatic navigation
  const navigate = useNavigate();
  
  // Form state management
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  // State for handling errors and loading
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // If user is already authenticated, redirect to dashboard/home
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  // Handle input changes and update form state
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,           // Spread previous state
      [name]: value      // Update the specific field that changed
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    
    // Clear any previous errors
    setError('');
    setIsLoading(true);

    // Basic client-side validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields');
      setIsLoading(false);
      return;
    }

    // Email format validation using regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      setIsLoading(false);
      return;
    }

    try {
      // Attempt to log in using the auth context function
      const result = await login(formData.email, formData.password);
      
      if (result.success) {
        // Login successful - navigate to dashboard
        navigate('/dashboard', { replace: true });
      } else {
        // Login failed - show error message
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      // Handle unexpected errors
      setError('An unexpected error occurred');
    } finally {
      // Always reset loading state
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form-wrapper">
        <form className="login-form" onSubmit={handleSubmit}>
          <h2 className="login-title">Welcome Back</h2>
          <p className="login-subtitle">Please sign in to your account</p>

          {/* Display error message if there is one */}
          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
              disabled={isLoading} // Disable input while loading
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              disabled={isLoading} // Disable input while loading
              required
            />
          </div>

          <button
            type="submit"
            className={`login-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>

          <div className="login-footer">
            <a href="#forgot-password" className="forgot-password-link">
              Forgot your password?
            </a>
          </div>

          {/* Demo credentials display */}
          <div className="demo-credentials">
            <p><strong>Demo Credentials:</strong></p>
            <p>Email: admin@example.com</p>
            <p>Password: password123</p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;