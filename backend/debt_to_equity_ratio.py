import yfinance as yf
import pandas as pd
import csv


def get_debt_to_equity_ratio():


    ticker = input("Please enter the ticker for which you would like to calculate the debt-to-equity ratio: ")

    #Creation data list for populating csv output file with debt to equity ration

    data = []

    """
    Calculates Apple's debt-to-equity ratio by year
    """
    # Create ticker object for Apple
    tckr = yf.Ticker(ticker)
    
    try:
        # Get annual balance sheet data
        balance_sheet = tckr.balance_sheet
        
        print("{t} DEBT-TO-EQUITY RATIO BY YEAR".format(t=ticker))
        print("=" * 40)
        
        # First, let's see what equity fields are available
        print("Available equity fields:")
        for field in balance_sheet.index:
            if any(word in field.lower() for word in ['equity', 'stockholder', 'shareholder']):
                print(f"  - {field}")
        print()
        
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
                print(f"{year}: {debt_to_equity:.2f}")
                data.append(dict(year = year, debt_to_equity = debt_to_equity, stock = ticker))
            else:
                print(f"{year}: Unable to calculate (missing equity data)")

    
    except Exception as e:
        print(f"Error: {e}")

    print(data)

    try:

        #Creation of csv empty file

        with open('Debt_to_equity.csv', 'w', newline='') as file:
            writer = csv.writer(file)

        with open('Debt_to_equity.csv', 'w', newline='') as csvfile:
            fieldnames = ['year', 'debt_to_equity', 'stock']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

            print("csv file for debt to equity ration created successfully @ your working directory; name of the file Debt_to.csv")

    except Exception as e:
        print(f"Error: {e}")     


#get_debt_to_equity_ratio()