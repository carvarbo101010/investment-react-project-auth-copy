import io
from datetime import datetime
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/api/debt-to-equity', methods=['POST'])
def calculate_debt_to_equity():
    try:
        data = request.json
        ticker = data.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400
        
        # Create ticker object
        tckr = yf.Ticker(ticker)
        
        # Get annual balance sheet data
        balance_sheet = tckr.balance_sheet
        
        if balance_sheet.empty:
            return jsonify({'error': f'No balance sheet data found for {ticker}'}), 404
        
        data_list = []
        
        # Calculate debt-to-equity ratio for each year
        for date in balance_sheet.columns:
            year = date.strftime('%Y')
            
            # Get debt components
            long_term_debt = balance_sheet.loc['Long Term Debt', date] if 'Long Term Debt' in balance_sheet.index else 0
            short_term_debt = balance_sheet.loc['Current Debt', date] if 'Current Debt' in balance_sheet.index else 0
            
            # Calculate total debt
            total_debt = (long_term_debt if pd.notna(long_term_debt) else 0) + (short_term_debt if pd.notna(short_term_debt) else 0)
            
            # Get total equity - try different possible field names
            equity_fields = ['Total Stockholder Equity', 'Stockholders Equity', 'Total Equity', 'Shareholders Equity']
            total_equity = None
            
            for field in equity_fields:
                if field in balance_sheet.index:
                    total_equity = balance_sheet.loc[field, date]
                    break
            
            # Calculate debt-to-equity ratio
            if pd.notna(total_equity) and total_equity != 0:
                debt_to_equity = total_debt / total_equity
                data_list.append({
                    'year': year,
                    'debt_to_equity': round(debt_to_equity, 2),
                    'stock': ticker
                })
        
        return jsonify({'data': data_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/debt-to-equity-csv', methods=['POST'])
def generate_debt_to_equity_csv():
    try:
        data = request.json
        ticker = data.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400
        
        # Create ticker object
        tckr = yf.Ticker(ticker)
        
        # Get annual balance sheet data
        balance_sheet = tckr.balance_sheet
        
        if balance_sheet.empty:
            return jsonify({'error': f'No balance sheet data found for {ticker}'}), 404
        
        data_list = []
        
        # Calculate debt-to-equity ratio for each year
        for date in balance_sheet.columns:
            year = date.strftime('%Y')
            
            # Get debt components
            long_term_debt = balance_sheet.loc['Long Term Debt', date] if 'Long Term Debt' in balance_sheet.index else 0
            short_term_debt = balance_sheet.loc['Current Debt', date] if 'Current Debt' in balance_sheet.index else 0
            
            # Calculate total debt
            total_debt = (long_term_debt if pd.notna(long_term_debt) else 0) + (short_term_debt if pd.notna(short_term_debt) else 0)
            
            # Get total equity - try different possible field names
            equity_fields = ['Total Stockholder Equity', 'Stockholders Equity', 'Total Equity', 'Shareholders Equity']
            total_equity = None
            
            for field in equity_fields:
                if field in balance_sheet.index:
                    total_equity = balance_sheet.loc[field, date]
                    break
            
            # Calculate debt-to-equity ratio
            if pd.notna(total_equity) and total_equity != 0:
                debt_to_equity = total_debt / total_equity
                data_list.append({
                    'year': year,
                    'debt_to_equity': round(debt_to_equity, 2),
                    'stock': ticker
                })
        
        # Create DataFrame and CSV
        df = pd.DataFrame(data_list)
        
        # Create a BytesIO object to hold the CSV data
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Send the CSV file
        return send_file(
            io.BytesIO(output.getvalue()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'debt_to_equity_{ticker}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cash-flow-csv', methods=['POST'])
def generate_cash_flow_csv(fcf_method="conservative"):
    try:
        data = request.json
        ticker = data.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400
        
        # Create ticker object
        tckr = yf.Ticker(ticker)
        
        # Get cash flow statement (annual data)
        cashflow = tckr.cashflow

        if cashflow.empty:
            return jsonify({'error': f'No cash flow data found for {ticker}'}), 404

        data_list = []
        
        # Process each year's data
        for column in cashflow.columns:
            year = column.year
            
            # Extract key cash flow metrics
            operating_cf = cashflow.loc['Operating Cash Flow', column] if 'Operating Cash Flow' in cashflow.index else 0
            investing_cf = cashflow.loc['Investing Cash Flow', column] if 'Investing Cash Flow' in cashflow.index else 0
            financing_cf = cashflow.loc['Financing Cash Flow', column] if 'Financing Cash Flow' in cashflow.index else 0
            
            # Calculate free cash flow (Operating CF - Capital Expenditures)
            capex = cashflow.loc['Capital Expenditures', column] if 'Capital Expenditures' in cashflow.index else 0
            
            # Calculate free cash flow with fallback logic for positive CAPEX
            capex = cashflow.loc['Capital Expenditures', column] if 'Capital Expenditures' in cashflow.index else 0

            # Apply different methods based on user preference
            if fcf_method == "conservative":
                if capex >= 0:  # Positive CAPEX (asset sales)
                    free_cashflow = operating_cf  # Exclude one-time gains
                    fcf_note = "excluding asset sales"
                else:  # Negative CAPEX (normal spending)
                    free_cashflow = operating_cf + capex
                    fcf_note = "standard calculation"
                    
            elif fcf_method == "inclusive":
                free_cashflow = operating_cf + capex  # Include everything
                fcf_note = "including all CAPEX"
                
            elif fcf_method == "hybrid":
                if capex >= 0:
                    free_cashflow = operating_cf + capex  # Include but flag it
                    fcf_note = f"includes +${capex/1e6:.0f}M asset sales"
                else:
                    free_cashflow = operating_cf + capex
                    fcf_note = "standard calculation"
            
            else:
                # Default fallback
                free_cashflow = operating_cf + capex
                fcf_note = "standard calculation"
            
            # Net change in cash
            net_change = operating_cf + investing_cf + financing_cf
            
            # Add to data list for CSV
            data_list.append({
                'year': year,
                'stock': ticker,
                'operating_cash_flow': operating_cf,
                'investing_cash_flow': investing_cf,
                'financing_cash_flow': financing_cf,
                'free_cash_flow': free_cashflow,
                'fcf_calculation': fcf_note,
                'capex': capex,
                'net_change_in_cash': net_change
            })
            
        # Create DataFrame and CSV
        df = pd.DataFrame(data_list)
        
        # Create a BytesIO object to hold the CSV data
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Send the CSV file
        return send_file(
            io.BytesIO(output.getvalue()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'cash_flow_{ticker}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/cash-earnings-growth-csv', methods=['POST'])
def generate_earnings_growth_csv():
    try:
        dticker = request.json
        ticker = dticker.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400
        
        # Create ticker object
        tckr = yf.Ticker(ticker)
        # Get annual financial data
        financials = tckr.financials

        if financials.empty:
            print(f"No financial data available for {ticker}")
            return None
        
        # Initialize results dictionary and data list for CSV
        earnings_data = {}
        data = []
        
        # Extract net income for each year
        net_income_by_year = {}
        
        for column in financials.columns:
            year = column.year
            net_income = financials.loc['Net Income', column] if 'Net Income' in financials.index else 0
            
            if pd.notna(net_income):
                net_income_by_year[year] = net_income
        
        # Sort years for proper growth calculation
        sorted_years = sorted(net_income_by_year.keys())
        
        # Calculate year-over-year earnings growth
        for i in range(1, len(sorted_years)):
            current_year = sorted_years[i]
            previous_year = sorted_years[i-1]
            
            current_earnings = net_income_by_year[current_year]
            previous_earnings = net_income_by_year[previous_year]
            
            # Calculate growth rate
            if previous_earnings != 0:
                growth_rate = ((current_earnings - previous_earnings) / abs(previous_earnings)) * 100
            else:
                growth_rate = float('inf') if current_earnings > 0 else float('-inf')
            
            earnings_data[current_year] = {
                'Net Income': current_earnings,
                'Previous Year Income': previous_earnings,
                'Growth Rate (%)': growth_rate,
                'Growth Amount': current_earnings - previous_earnings
            }
            
            # Add to data list for CSV
            data.append({
                'year': current_year,
                'net_income': current_earnings,
                'previous_year_income': previous_earnings,
                'growth_rate_percent': growth_rate,
                'growth_amount': current_earnings - previous_earnings,
                'stock': ticker
            })
        
        
            
        # Create DataFrame and CSV
        df = pd.DataFrame(data)
        
        # Create a BytesIO object to hold the CSV data
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Send the CSV file
        return send_file(
            io.BytesIO(output.getvalue()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'cash_flow_{ticker}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/roe-csv', methods=['POST'])
def generate_roe_csv():
    try:
        dticker = request.json
        ticker = dticker.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400
        
        # Create ticker object
        tckr = yf.Ticker(ticker)
        financials = tckr.financials
        balance_sheet = tckr.balance_sheet
        
        if financials.empty or balance_sheet.empty:
            print(f"No financial or balance sheet data available for {ticker_symbol}")
            return None, None
        
        # Initialize results dictionary and data list for CSV
        roe_data = {}
        data = []
        
        # Process each year's data
        for column in financials.columns:
            year = column.year
            
            # Get net income from income statement
            net_income = financials.loc['Net Income', column] if 'Net Income' in financials.index else 0
            
            # Get total equity from balance sheet - try different possible field names
            equity_fields = ['Total Stockholder Equity', 'Stockholders Equity', 'Total Equity', 'Shareholders Equity']
            total_equity = None
            
            # Find matching column in balance sheet for the same year
            balance_sheet_column = None
            for bs_col in balance_sheet.columns:
                if bs_col.year == year:
                    balance_sheet_column = bs_col
                    break
            
            if balance_sheet_column is not None:
                for field in equity_fields:
                    if field in balance_sheet.index:
                        total_equity = balance_sheet.loc[field, balance_sheet_column]
                        break
            
            # Calculate ROE
            if pd.notna(net_income) and pd.notna(total_equity) and total_equity != 0:
                roe = (net_income / total_equity) * 100
                
                roe_data[year] = {
                    'Net Income': net_income,
                    'Total Equity': total_equity,
                    'ROE (%)': roe
                }
                
                # Add to data list for CSV
                data.append({
                    'year': year,
                    'net_income': net_income,
                    'total_equity': total_equity,
                    'roe_percent': roe,
                    'stock': ticker
                })
            else:
                print(f"{year}: Unable to calculate ROE (missing data)")
        
                
        # Create DataFrame and CSV
        df = pd.DataFrame(data)
        
        # Create a BytesIO object to hold the CSV data
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Send the CSV file
        return send_file(
            io.BytesIO(output.getvalue()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'cash_flow_{ticker}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Side Note: This condition ensures the code below only runs when the script is executed directly
    # Not when it's imported as a module
    
    app.run(debug=True, port=5000)
    # Side Note: debug=True enables auto-reload when code changes and shows detailed error messages
    # port=5000 sets the server to run on localhost:5000