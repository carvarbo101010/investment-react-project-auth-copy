import yfinance as yf
import pandas as pd
from datetime import datetime

def get_annual_cashflow(ticker_symbol, fcf_method="conservative"):
    """
    Calculate annual cash flow for a given ticker using yfinance API.
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        fcf_method (str): Method for handling positive CAPEX
            - "conservative": Exclude asset sales from FCF (default)
            - "inclusive": Include all CAPEX regardless of sign
            - "hybrid": Use standard calc for negative CAPEX, note positive CAPEX
    
    Returns:
        dict: Dictionary containing cash flow data organized by year
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # Get cash flow statement (annual data)
        cashflow = ticker.cashflow
        
        if cashflow.empty:
            print(f"No cash flow data available for {ticker_symbol}")
            return None
        
        # Initialize results dictionary
        annual_cashflow = {}
        
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
            
            annual_cashflow[year] = {
                'Operating Cash Flow': operating_cf,
                'Investing Cash Flow': investing_cf,
                'Financing Cash Flow': financing_cf,
                'Free Cash Flow': free_cashflow,
                'FCF Calculation': fcf_note,
                'CAPEX': capex,
                'Net Change in Cash': net_change
            }
        
        return annual_cashflow
    
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {str(e)}")
        return None

def display_cashflow_summary(ticker_symbol, cashflow_data):
    """
    Display a formatted summary of cash flow data.
    
    Args:
        ticker_symbol (str): Stock ticker symbol
        cashflow_data (dict): Cash flow data dictionary
    """
    if not cashflow_data:
        return
    
    print(f"\n{'='*60}")
    print(f"ANNUAL CASH FLOW SUMMARY FOR {ticker_symbol.upper()}")
    print(f"{'='*60}")
    print(f"{'Year':<8} {'Operating':<12} {'Investing':<12} {'Financing':<12} {'Free CF':<12} {'CAPEX':<12} {'Net Change':<12}")
    print(f"{'    ':<8} {'CF (M)':<12} {'CF (M)':<12} {'CF (M)':<12} {'(M)':<12} {'(M)':<12} {'(M)':<12}")
    print("-" * 80)
    
    # Sort years in descending order (most recent first)
    for year in sorted(cashflow_data.keys(), reverse=True):
        data = cashflow_data[year]
        print(f"{year:<8} "
              f"{data['Operating Cash Flow']/1e6:>10.0f}  "
              f"{data['Investing Cash Flow']/1e6:>10.0f}  "
              f"{data['Financing Cash Flow']/1e6:>10.0f}  "
              f"{data['Free Cash Flow']/1e6:>10.0f}  "
              f"{data['CAPEX']/1e6:>10.0f}  "
              f"{data['Net Change in Cash']/1e6:>10.0f}")
        
        # Show FCF calculation notes if any special handling occurred
        if data['FCF Calculation'] != "standard calculation":
            print(f"         Note: FCF {data['FCF Calculation']}")

def main():
    
    """
    Main function to run the cash flow calculator.
    """
    # Example usage
    ticker = input("Enter ticker symbol (e.g., AAPL, MSFT, GOOGL): ").upper().strip()
    
    print(f"\nFetching cash flow data for {ticker}...")
    
    # Get cash flow data
    cashflow_data = get_annual_cashflow(ticker)
    
    if cashflow_data:
        # Display summary
        display_cashflow_summary(ticker, cashflow_data)
        
        # Optional: Return as DataFrame for further analysis
        df = pd.DataFrame(cashflow_data).T
        df = df.sort_index(ascending=False)  # Most recent year first
        
        print(f"\nDetailed DataFrame:")
        print(df)
        
        return df
    else:
        print("Failed to retrieve cash flow data.")
        return None

# Example usage for specific tickers
#def analyze_multiple_tickers(tickers):
    """
    Analyze cash flow for multiple tickers.
    
    Args:
        tickers (list): List of ticker symbols
    """
    #results = {}
    
    #for ticker in tickers:
        #print(f"\nAnalyzing {ticker}...")
        #cashflow_data = get_annual_cashflow(ticker)
        #if cashflow_data:
            #results[ticker] = cashflow_data
            #display_cashflow_summary(ticker, cashflow_data)
    
    #return results

if __name__ == "__main__":
    # Run the main function
    df = main()

    df.to_csv('Cash_Flow.csv', index=False)
    
    # Example of analyzing multiple tickers
    # tickers = ['AAPL', 'MSFT', 'GOOGL']
    # results = analyze_multiple_tickers(tickers)