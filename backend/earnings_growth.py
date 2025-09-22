import yfinance as yf
import pandas as pd
import csv
from datetime import datetime

def get_earnings_growth(ticker_symbol):
    """
    Calculate earnings growth for a given ticker using yfinance API.
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        dict: Dictionary containing earnings growth data organized by year
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Get annual financial data
        financials = ticker.financials
        
        if financials.empty:
            print(f"No financial data available for {ticker_symbol}")
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
                'stock': ticker_symbol
            })
        
        return earnings_data, data
    
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {str(e)}")
        return None, None

def display_earnings_growth_summary(ticker_symbol, earnings_data):
    """
    Display a formatted summary of earnings growth data.
    
    Args:
        ticker_symbol (str): Stock ticker symbol
        earnings_data (dict): Earnings growth data dictionary
    """
    if not earnings_data:
        return
    
    print(f"\n{'='*70}")
    print(f"EARNINGS GROWTH SUMMARY FOR {ticker_symbol.upper()}")
    print(f"{'='*70}")
    print(f"{'Year':<8} {'Net Income':<15} {'Previous Year':<15} {'Growth Rate':<12} {'Growth Amount':<15}")
    print(f"{'    ':<8} {'(M)':<15} {'(M)':<15} {'(%)':<12} {'(M)':<15}")
    print("-" * 70)
    
    # Sort years in descending order (most recent first)
    for year in sorted(earnings_data.keys(), reverse=True):
        data = earnings_data[year]
        growth_rate = data['Growth Rate (%)']
        
        # Format growth rate display
        if growth_rate == float('inf'):
            growth_display = "∞"
        elif growth_rate == float('-inf'):
            growth_display = "-∞"
        else:
            growth_display = f"{growth_rate:>8.1f}"
        
        print(f"{year:<8} "
              f"{data['Net Income']/1e6:>13.0f}  "
              f"{data['Previous Year Income']/1e6:>13.0f}  "
              f"{growth_display}  "
              f"{data['Growth Amount']/1e6:>13.0f}")

def calculate_average_growth_rate(earnings_data):
    """
    Calculate the average earnings growth rate over the available years.
    
    Args:
        earnings_data (dict): Earnings growth data dictionary
    
    Returns:
        float: Average growth rate percentage
    """
    if not earnings_data:
        return None
    
    valid_growth_rates = []
    for year_data in earnings_data.values():
        growth_rate = year_data['Growth Rate (%)']
        if growth_rate not in [float('inf'), float('-inf')] and pd.notna(growth_rate):
            valid_growth_rates.append(growth_rate)
    
    if valid_growth_rates:
        return sum(valid_growth_rates) / len(valid_growth_rates)
    return None

def save_earnings_data_to_csv(data, filename='Earnings_Growth.csv'):
    """
    Save earnings growth data to CSV file.
    
    Args:
        data (list): List of earnings data dictionaries
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['year', 'net_income', 'previous_year_income', 'growth_rate_percent', 'growth_amount', 'stock']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"\nEarnings growth data saved to {filename}")
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    """
    Main function to run the earnings growth calculator.
    """
    ticker = input("Enter ticker symbol (e.g., AAPL, MSFT, GOOGL): ").upper().strip()
    
    print(f"\nFetching earnings data for {ticker}...")
    
    # Get earnings growth data
    earnings_data, csv_data = get_earnings_growth(ticker)
    
    if earnings_data and csv_data:
        # Display summary
        display_earnings_growth_summary(ticker, earnings_data)
        
        # Calculate and display average growth rate
        avg_growth = calculate_average_growth_rate(earnings_data)
        if avg_growth is not None:
            print(f"\nAverage Earnings Growth Rate: {avg_growth:.2f}%")
        
        # Save to CSV
        save_earnings_data_to_csv(csv_data)
        
        # Optional: Return as DataFrame for further analysis
        df = pd.DataFrame(csv_data)
        df = df.sort_values('year', ascending=False)  # Most recent year first
        
        print(f"\nDetailed DataFrame:")
        print(df)
        
        return df
    else:
        print("Failed to retrieve earnings data.")
        return None

if __name__ == "__main__":
    df = main()