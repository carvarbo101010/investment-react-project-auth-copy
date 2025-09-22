# Investment Analysis Dashboard

A comprehensive React-based investment analysis tool with authentication, featuring key financial metrics analysis based on Peter Lynch's investment principles from "One Up On Wall Street".

## Features

### Authentication System
- **Secure Login/Logout**: Protected routes with session persistence
- **Demo Credentials**:
  - **Username**: `admin@example.com`
  - **Password**: `password123`
- **Session Management**: Automatic session restoration on browser refresh
- **Route Protection**: Investment dashboard only accessible after authentication

### Investment Analysis Tools
- **Debt-to-Equity Ratio Analysis**: Calculate and export debt ratios over time
- **Cash Flow Analysis**: Track company cash flow patterns
- **Earnings Growth Analysis**: Monitor earnings growth trends
- **Return on Equity (ROE)**: Analyze company profitability metrics
- **CSV Export**: Download all analysis results in CSV format
- **Real-time Data**: Connect to financial data APIs for live analysis

### Educational Content
- **Peter Lynch Biography**: Learn from the legendary investor's principles
- **Investment Philosophy**: Implementation of "One Up On Wall Street" concepts

## Quick Start

1. **Clone and install**:
   ```bash
   git clone <your-repo-url>
   cd investment-react-project-auth
   npm install
   ```

2. **Start backend server**:
   ```bash
   cd backend
   python app.py
   ```

3. **Start frontend**:
   ```bash
   npm start
   ```

4. **Login**: Go to `http://localhost:3000` and use:
   - Email: `admin@example.com`
   - Password: `password123`

## Project Structure

```
investment-react-project-auth/
├── src/
│   ├── components/
│   │   ├── Login.js              # Authentication login form
│   │   ├── Login.css             # Login styling
│   │   ├── InvestmentDashboard.js # Main investment analysis interface
│   │   ├── ProtectedRoute.js     # Route protection component
│   │   ├── Dashboard.js          # Alternative dashboard component
│   │   └── Dashboard.css         # Dashboard styling
│   ├── contexts/
│   │   └── AuthContext.js        # Authentication state management
│   ├── App.js                    # Main app with routing
│   ├── App.css                   # Main application styling
│   └── index.js                  # Application entry point
├── backend/
│   ├── app.py                    # Main Flask server
│   ├── debt_to_equity_ratio.py   # Debt-to-equity calculations
│   ├── cash_flow.py              # Cash flow analysis
│   ├── earnings_growth.py        # Earnings growth calculations
│   └── roe_calculator.py         # Return on equity calculations
├── public/
│   ├── index.html                # HTML template
│   └── images/
│       └── peter.jpg             # Peter Lynch photo
├── standalone.html               # Browser-ready version (no npm required)
└── README.md                     # This file
```

## Available Scripts

- **`npm start`**: Runs development server on http://localhost:3000
- **`npm run build`**: Creates production build
- **`npm test`**: Runs test suite
- **`npm run eject`**: Ejects from Create React App (irreversible)

## Backend API

### Technology Stack
- **Framework**: Flask (Python)
- **Data Processing**: pandas, numpy
- **Financial Data**: Integration with financial data providers
- **CORS**: Enabled for frontend communication

### API Endpoints

All endpoints require POST requests with JSON body containing `{"ticker": "SYMBOL"}`

- **`POST /api/debt-to-equity`**: Calculate debt-to-equity ratios
- **`POST /api/debt-to-equity-csv`**: Export debt-to-equity data as CSV
- **`POST /api/cash-flow-csv`**: Export cash flow analysis as CSV
- **`POST /api/cash-earnings-growth-csv`**: Export earnings growth data as CSV
- **`POST /api/roe-csv`**: Export ROE calculations as CSV

#### Example Request
```javascript
const response = await axios.post('http://localhost:5000/api/debt-to-equity', {
  ticker: 'AAPL'
});
```

#### Response Format
```json
{
  "data": [
    {
      "year": 2023,
      "debt_to_equity": 1.45,
      "total_debt": 123456789,
      "total_equity": 85234567
    }
  ]
}
```

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask pandas numpy requests flask-cors
   ```

4. **Run the server**:
   ```bash
   python app.py
   ```

Server runs on `http://localhost:5000`

## Frontend

### Technology Stack
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS3 with modern features
- **Build Tool**: Create React App

### Key Components

#### Authentication System
- **AuthContext**: Centralized authentication state management
- **Login Component**: Beautiful gradient login form with validation
- **ProtectedRoute**: Higher-order component for route protection
- **Session Persistence**: Automatic login restoration using localStorage

#### Investment Dashboard
- **Multi-metric Analysis**: Support for 4 different financial metrics
- **CSV Export**: One-click download for all analysis types
- **Real-time Updates**: Live data integration with backend APIs
- **Responsive Design**: Works on desktop and mobile devices

## Authentication Details

### Login Process
1. User enters credentials on login page
2. Frontend validates email format and required fields
3. Credentials checked against mock authentication system
4. On success: JWT token and user data stored in localStorage
5. User redirected to protected investment dashboard
6. Session automatically restored on browser refresh

### Security Features
- **Route Protection**: Unauthenticated users redirected to login
- **Session Management**: Secure token-based authentication
- **Input Validation**: Client-side validation for all forms
- **Error Handling**: Comprehensive error messages for failed logins

### Demo Account
- **Email**: admin@example.com
- **Password**: password123
- **User Name**: Admin (displayed in dashboard)

## Development Workflow

### Running the Full Application
1. **Start Backend**: 
   ```bash
   cd backend && python app.py
   ```
2. **Start Frontend**: 
   ```bash
   npm start
   ```
3. **Access Application**: Navigate to `http://localhost:3000`

### Testing Authentication
1. Go to `http://localhost:3000`
2. You'll be redirected to login page
3. Use demo credentials: `admin@example.com` / `password123`
4. After login, access the investment dashboard
5. Test logout functionality with top-right logout button

## Alternative Access Methods

### Standalone Version
If npm/Node.js issues occur, use `standalone.html`:
- **No setup required**: Open directly in browser
- **Full functionality**: Complete authentication and analysis features
- **CDN dependencies**: Uses React, Axios from CDN
- **File location**: `./standalone.html`

### Production Build
For deployment:
```bash
npm run build
```
Serves optimized static files from `build/` directory.

## Investment Philosophy

This tool implements principles from Peter Lynch's "One Up On Wall Street":
- **Fundamental Analysis**: Focus on key financial ratios
- **Long-term Perspective**: Multi-year data analysis
- **Simplicity**: Easy-to-understand metrics
- **Data-driven Decisions**: Quantitative analysis tools

## Troubleshooting

### npm start Issues
If you get `bash: /snap/bin/npm: No such file or directory`:

1. **Fix PATH with aliases**:
   ```bash
   echo 'alias npm="/usr/bin/npm"' >> ~/.bashrc
   echo 'alias node="/usr/bin/node"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Or use full path**:
   ```bash
   /usr/bin/npm start
   ```

### Backend Connection Issues
- Ensure Flask server is running on `http://localhost:5000`
- Check CORS configuration in backend
- Verify API endpoints are accessible

### Common Issues
- **Authentication not working**: Check browser localStorage for stored tokens
- **CSV downloads failing**: Ensure backend server is running
- **Styling issues**: Clear browser cache and reload

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

This project is licensed under the MIT License.

---

**Happy Investing! 📈**