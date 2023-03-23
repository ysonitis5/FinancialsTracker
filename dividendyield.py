import ssl
import requests
import pandas as pd
import time
import csv
import html5lib
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'key'

def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url, header=0)[0]
    symbols = table['Symbol'].tolist()
    return symbols

def get_nasdaq_symbols():
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    table = pd.read_html(url, header=0, match='Ticker')[0]
    symbols = table['Ticker'].tolist()
    return symbols

def get_dow_symbols():
    url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
    table = pd.read_html(url, header=0, match='Symbol')[0]
    symbols = table['Symbol'].tolist()
    return symbols


def get_dividend_info(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    company_name = data.get('Name', 'N/A')
    dividend = float(data.get('DividendPerShare', 0))
    price = float(data.get('MarketCapitalization', 0)) / float(data.get('SharesOutstanding', 1))
    dividend_yield = dividend / price * 100 if price > 0 else 0
    min_price_for_7_percent_yield = dividend / 0.07 if dividend > 0 else 0

    return company_name, dividend, dividend_yield, price, min_price_for_7_percent_yield

stock_symbols = get_sp500_symbols() + get_nasdaq_symbols() + get_dow_symbols()
stock_symbols = list(set(stock_symbols))  # Remove duplicates


stocks_dividend_info = []

for symbol in stock_symbols:
    company_name, dividend, dividend_yield, price, min_price_for_7_percent_yield = get_dividend_info(symbol)
    investment_needed = (1000 / dividend) * price if dividend > 0 else 0
    stocks_dividend_info.append((symbol, company_name, dividend, dividend_yield, price, min_price_for_7_percent_yield, investment_needed))
    print(f"{symbol}: {company_name}, Dividend: ${dividend:.2f}, Dividend Yield: {dividend_yield:.2f}%, Price: ${price:.2f}, Min Price for 7% Yield: ${min_price_for_7_percent_yield:.2f}, Investment Needed: ${investment_needed:.2f}")

    # Add a delay between requests to respect the API rate limit (5 requests per minute for free accounts)
    time.sleep(12)

# Sort stocks by dividend yield in descending order
sorted_stocks = sorted(stocks_dividend_info, key=lambda x: x[3], reverse=True)

# Save the data to a CSV file
with open('dividend_yields.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Symbol', 'Company Name', 'Dividend', 'Dividend Yield', 'Price', 'Min Price for 7% Yield', 'Investment Needed'])
    for row in sorted_stocks:
        symbol, company_name, dividend, dividend_yield, price, min_price_for_7_percent_yield, investment_needed = row
        csvwriter.writerow([symbol, company_name, f"${dividend:.2f}", f"{dividend_yield:.2f}%", f"${price:.2f}", f"${min_price_for_7_percent_yield:.2f}", f"${investment_needed:.2f}"])

print("Stocks with the best dividend yields:")
for symbol, company_name, dividend, dividend_yield, price, min_price_for_7_percent_yield, investment_needed in sorted_stocks:
    print(f"{symbol}: {company_name}, Dividend: ${dividend:.2f}, Dividend Yield: {dividend_yield:.2f}%, Price: ${price:.2f}, Min Price for 7% Yield: ${min_price_for_7_percent_yield:.2f}, Investment Needed: ${investment_needed:.2f}")
