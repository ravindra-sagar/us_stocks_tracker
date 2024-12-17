import yfinance as yf
import pandas as pd
import duckdb
import requests
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
import csv
import time

# Getting all US stocks in NYSE and NASDAQ
def get_us_stocks(api_key):
    base_url = "https://www.alphavantage.co/query"
    function = "LISTING_STATUS"
    # Construct the API request URL
    api_url = f"{base_url}?function={function}&apikey={api_key}"
    # Download an decoding the list of stocks
    with requests.Session() as s:
        download = s.get(api_url)
        decoded_content = download.content.decode('utf-8')
        raw_csv = csv.reader(decoded_content.splitlines(), delimiter=',')
        raw_list = list(raw_csv)
        raw_df = pd.DataFrame(raw_list)
        raw_df.columns = ['Ticker', 'Company', 'Exchange', 'Asset Type', 'IPO Date', 'Delisting Date', 'Status']
        raw_df = raw_df[raw_df['Asset Type']== 'Stock']
        raw_df = raw_df[(raw_df['Exchange']== 'NASDAQ') | (raw_df['Exchange']== 'NYSE')]
        final_df = raw_df[['Ticker', 'Company', 'Exchange', 'Asset Type']]
    print("Fetching all US stocks in NYSE and NASDAQ complete")
    return final_df

# Uploading stock list into DuckDB
def upload_stock_list_in_duckdb (us_stocks, db_file):
    # Connecting to DuckDB
    database_name = db_file
    conn = duckdb.connect(database_name)
    conn.execute(f"DROP TABLE IF EXISTS company_list")
    conn.execute(f"CREATE TABLE company_list AS SELECT * FROM us_stocks")
    conn.close()
    print("Uploaded stock list into DuckDB")


# Getting last 30-day adjusted close price, Outstanding shares and Market Cap from Yahoo Finance
def get_financial_data(tickers):
    print(f"Fetching daily financial information")
    # Calculate the date range for the last month
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    # Create an empty list to store the results
    result_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        # Check if data exists
        historical_data = yf.download(ticker, start_date, end_date)
        if historical_data.empty:
            print(f"No data found for {ticker}")
        else:
            # Get Adjusted Close
            adjusted_close = historical_data['Adj Close']
            # Get Market Cap 
            market_cap = stock.info.get('marketCap', None)
            # Get Outstanding Shares
            shares_outstanding = stock.info.get('sharesOutstanding', None)
            # Add each day's data to the result list
            for adj_close in adjusted_close.items():
                for date in adj_close[1].index.tolist():
                    result_data.append({
                        'Ticker': ticker,
                        'Date': date,
                        'Adjusted Close': adj_close[1][date],
                        'Outstanding Shares': shares_outstanding
                    })
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(result_data)
    return df

# Uploading stock list to DuckDB
def upload_financial_info_in_duckdb(daily_data, db_file):
    # Connecting to DuckDB
    database_name = db_file
    conn = duckdb.connect(database_name)
    conn.execute(f"DROP TABLE IF EXISTS daily_market_cap")
    conn.execute(f"CREATE TABLE daily_market_cap AS SELECT * FROM daily_data") 
    conn.close()
    print("Uploaded financial information into DuckDB")

def fetch_and_store_market_data(db_file, api_key):
    
    # Part 1: Fetch list of US stock tickers in NASDAQ and NYSE
    us_stocks = get_us_stocks(api_key)
    us_stocks_list = us_stocks['Ticker'].to_list()
    
    # Part 2: Upload list of Companies into DuckDB
    if not us_stocks.empty:
        upload_stock_list_in_duckdb(us_stocks, db_file)
    else:
        print("No data to store in DuckDB")
    
    # Part 3: Get Adjusted close price, Outstanding Shares and Market Capitalization
    daily_data = get_financial_data(us_stocks_list)

    # Part 4: Upload financial information into DuckDB
    if not us_stocks_list == []:
        upload_financial_info_in_duckdb(daily_data, db_file)
    else:
        print("No data to store in DuckDB")