// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { checkUserAuthorization, getUserFromCSV } from '../utils/csvAuth';

// Create a context for authentication state management
const AuthContext = createContext();

// Custom hook to use the auth context - makes it easier to access auth state in components
export const useAuth = () => {
  const context = useContext(AuthContext);
  // Throw error if hook is used outside of AuthProvider
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// AuthProvider component that wraps the app and provides auth state to all children
export const AuthProvider = ({ children }) => {
  // State to track if user is authenticated
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // State to store user information
  const [user, setUser] = useState(null);
  // Loading state for async operations
  const [loading, setLoading] = useState(true);

  // Check if user is already logged in when component mounts
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (token && userData) {
      // If token exists, user is authenticated
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
    // Set loading to false after checking
    setLoading(false);
  }, []);

  // Login function - this is where you'd typically make an API call
  const login = async (email, password) => {
    try {
      // Simulate API call (replace with your actual authentication endpoint)
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store token and user data in localStorage for persistence
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userData', JSON.stringify(data.user));
        
        // Update state
        setIsAuthenticated(true);
        setUser(data.user);
        return { success: true };
      } else {
        // Handle login failure
        const errorData = await response.json();
        return { success: false, error: errorData.message };
      }
    } catch (error) {
      // Handle network errors
      return { success: false, error: 'Network error occurred' };
    }
  };

  // CSV-based login function
  const csvLogin = async (email, password) => {
    try {
      // Check if user is authorized via CSV
      const isAuthorized = await checkUserAuthorization(email);

      if (!isAuthorized) {
        return { success: false, error: 'User not authorized. Please contact administrator.' };
      }

      // Get user details from CSV
      const userData = await getUserFromCSV(email);

      if (!userData) {
        return { success: false, error: 'User data not found.' };
      }

      // For demo purposes, accept any password for authorized users
      // In production, you'd verify the password against a secure backend
      if (password && password.length >= 6) {
        const userInfo = {
          id: Date.now(), // Generate a simple ID
          email: userData.email,
          name: userData.name,
          role: userData.role
        };

        localStorage.setItem('authToken', 'csv-auth-token');
        localStorage.setItem('userData', JSON.stringify(userInfo));

        setIsAuthenticated(true);
        setUser(userInfo);
        return { success: true };
      } else {
        return { success: false, error: 'Password must be at least 6 characters long.' };
      }
    } catch (error) {
      console.error('CSV Login error:', error);
      return { success: false, error: 'Authentication service error. Please try again.' };
    }
  };

  // Logout function
  const logout = () => {
    // Remove data from localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    
    // Reset state
    setIsAuthenticated(false);
    setUser(null);
  };

  // Value object that will be provided to all consuming components
  const value = {
    isAuthenticated,
    user,
    login: csvLogin, // CSV-based authentication
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};