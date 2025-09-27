// src/utils/csvAuth.js
import Papa from 'papaparse';

class CSVAuthManager {
  constructor() {
    this.authorizedUsers = [];
    this.isLoaded = false;
  }

  // Load and parse the CSV file
  async loadAuthorizedUsers() {
    try {
      const response = await fetch('/authorized_users.csv');
      const csvText = await response.text();

      return new Promise((resolve, reject) => {
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            this.authorizedUsers = results.data.filter(user =>
              user.email && user.email.trim() !== ''
            );
            this.isLoaded = true;
            console.log('Authorized users loaded:', this.authorizedUsers);
            resolve(this.authorizedUsers);
          },
          error: (error) => {
            console.error('Error parsing CSV:', error);
            reject(error);
          }
        });
      });
    } catch (error) {
      console.error('Error loading CSV file:', error);
      throw error;
    }
  }

  // Check if a user is authorized
  isUserAuthorized(email) {
    if (!this.isLoaded) {
      console.warn('CSV not loaded yet. Call loadAuthorizedUsers() first.');
      return false;
    }

    const user = this.authorizedUsers.find(
      user => user.email.toLowerCase() === email.toLowerCase()
    );

    return !!user;
  }

  // Get user details from CSV
  getUserDetails(email) {
    if (!this.isLoaded) {
      console.warn('CSV not loaded yet. Call loadAuthorizedUsers() first.');
      return null;
    }

    const user = this.authorizedUsers.find(
      user => user.email.toLowerCase() === email.toLowerCase()
    );

    return user || null;
  }

  // Get all authorized users (admin only)
  getAllAuthorizedUsers() {
    return this.authorizedUsers;
  }
}

// Create a singleton instance
export const csvAuthManager = new CSVAuthManager();

// Helper function for easy usage
export const checkUserAuthorization = async (email) => {
  if (!csvAuthManager.isLoaded) {
    await csvAuthManager.loadAuthorizedUsers();
  }
  return csvAuthManager.isUserAuthorized(email);
};

export const getUserFromCSV = async (email) => {
  if (!csvAuthManager.isLoaded) {
    await csvAuthManager.loadAuthorizedUsers();
  }
  return csvAuthManager.getUserDetails(email);
};