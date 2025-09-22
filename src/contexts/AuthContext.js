// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

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

  // Mock login function for demonstration (remove this when you have a real backend)
  const mockLogin = (email, password) => {
    // Simple validation for demo purposes
    if (email === 'admin@example.com' && password === 'password123') {
      const userData = { id: 1, email, name: 'Admin' };
      
      localStorage.setItem('authToken', 'mock-jwt-token');
      localStorage.setItem('userData', JSON.stringify(userData));
      
      setIsAuthenticated(true);
      setUser(userData);
      return { success: true };
    }
    return { success: false, error: 'Invalid credentials' };
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
    login: mockLogin, // Use 'login' for real API, 'mockLogin' for demo
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};