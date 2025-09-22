import yfinance as yf
import pandas as pd
import csv
from datetime import datetime

def get_roe_historical(ticker_symbol):
    """
    Calculate Return on Equity (ROE) for a given ticker using yfinance API.
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        tuple: (roe_data dict, csv_data list) containing ROE data organized by year
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Get annual financial data
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        
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
                    'stock': ticker_symbol
                })
            else:
                print(f"{year}: Unable to calculate ROE (missing data)")
        
        return roe_data, data
    
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {str(e)}")
        return None, None

def display_roe_summary(ticker_symbol, roe_data):
    """
    Display a formatted summary of ROE data.
    
    Args:
        ticker_symbol (str): Stock ticker symbol
        roe_data (dict): ROE data dictionary
    """
    if not roe_data:
        return
    
    print(f"\n{'='*70}")
    print(f"RETURN ON EQUITY (ROE) SUMMARY FOR {ticker_symbol.upper()}")
    print(f"{'='*70}")
    print(f"{'Year':<8} {'Net Income':<15} {'Total Equity':<15} {'ROE (%)':<12}")
    print(f"{'    ':<8} {'(M)':<15} {'(M)':<15} {'    ':<12}")
    print("-" * 60)
    
    # Sort years in descending order (most recent first)
    for year in sorted(roe_data.keys(), reverse=True):
        data = roe_data[year]
        print(f"{year:<8} "
              f"{data['Net Income']/1e6:>13.0f}  "
              f"{data['Total Equity']/1e6:>13.0f}  "
              f"{data['ROE (%)']:>8.2f}")

def calculate_average_roe(roe_data):
    """
    Calculate the average ROE over the available years.
    
    Args:
        roe_data (dict): ROE data dictionary
    
    Returns:
        float: Average ROE percentage
    """
    if not roe_data:
        return None
    
    roe_values = [year_data['ROE (%)'] for year_data in roe_data.values()]
    
    if roe_values:
        return sum(roe_values) / len(roe_values)
    return None

def save_roe_data_to_csv(data, filename='ROE_Historical.csv'):
    """
    Save ROE data to CSV file.
    
    Args:
        data (list): List of ROE data dictionaries
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['year', 'net_income', 'total_equity', 'roe_percent', 'stock']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"\nROE data saved to {filename}")
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    """
    Main function to run the ROE calculator.
    """
    ticker = input("Enter ticker symbol (e.g., AAPL, MSFT, GOOGL): ").upper().strip()
    
    print(f"\nFetching ROE data for {ticker}...")
    
    # Get ROE data
    roe_data, csv_data = get_roe_historical(ticker)
    
    if roe_data and csv_data:
        # Display summary
        display_roe_summary(ticker, roe_data)
        
        # Calculate and display average ROE
        avg_roe = calculate_average_roe(roe_data)
        if avg_roe is not None:
            print(f"\nAverage ROE: {avg_roe:.2f}%")
        
        # Save to CSV
        save_roe_data_to_csv(csv_data)
        
        # Optional: Return as DataFrame for further analysis
        df = pd.DataFrame(csv_data)
        df = df.sort_values('year', ascending=False)  # Most recent year first
        
        print(f"\nDetailed DataFrame:")
        print(df)
        
        return df
    else:
        print("Failed to retrieve ROE data.")
        return None

if __name__ == "__main__":
    df = main()