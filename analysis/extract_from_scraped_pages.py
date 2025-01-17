# This script extracts financial data from HTML files for a list of stock tickers.
# Functions:
#     load_tickers(file_path):
#         Loads ticker symbols from a JSON file.
#             file_path (str): The path to the JSON file containing ticker symbols.
#             list: A list of ticker symbols.
#     extract_data_from_html(file_path):
#     extract_equity_data(soup):
#         Extracts equity data from a BeautifulSoup object.
#         This function parses a BeautifulSoup object to extract equity data such as Market Cap and Shares.
#             soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.
#             dict: A dictionary containing the extracted equity data.
# Main Execution:
#     - Loads ticker symbols from a JSON file.
#     - Checks for the availability of HTML files for the tickers.
#     - Extracts financial data from the available HTML files.
#     - Prints the extracted financial data in JSON format.
import json
import os
from bs4 import BeautifulSoup
import re

def load_tickers(file_path):
    with open(file_path, 'r') as file:
        tickers = json.load(file)
    return tickers

def extract_data_from_html(file_path):
    """
    Extracts financial data from an HTML file.
    This function reads an HTML file, parses it using BeautifulSoup, and extracts specific financial data such as
    Sales, EPS, stock price, and equity data. The extracted data is returned as a dictionary.
    Args:
        file_path (str): The path to the HTML file to be parsed.
    Returns:
        dict: A dictionary containing the extracted financial data. The keys may include 'Sales', 'EPS', 'Price', 
              and other equity data extracted by the `extract_equity_data` function.
    """
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    data = {}
    financial_tab = soup.find('div', id='financialTab')
    if financial_tab:
        annual_panel = financial_tab.find('div', class_='tabs__panel tabs__panel--selected', attrs={'data-name': 'Annual'})
        if annual_panel:
            rows = annual_panel.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    key = columns[0].text.strip()
                    if key in ["Sales", "EPS"]:
                        data[key] = [col.text.strip().replace(',', '') for col in columns[1:]]
    
    equity_data = extract_equity_data(soup)
    data.update(equity_data)
    
    # Extract stock price
    quote_close = soup.find('div', class_='quote__close')
    if quote_close:
        price_text = quote_close.text.strip()
        price = re.findall(r'\d+\.\d+', price_text)
        if price:
            data['price'] = price[0]
    
    return data

def extract_equity_data(soup):
    equity_data = {}
    equity_section = soup.find('div', id='equity')
    if equity_section:
        stats_items = equity_section.find_all('div', class_='stats_item')
        for item in stats_items:
            label = item.find('div', class_='stats_label').text.strip()
            value = item.find('div', class_='stats_value').text.strip().replace(',', '')
            if label == "Market Cap (000's)":
                equity_data['market_cap'] = str(float(value) * 1000)
            elif label == "Shares":
                equity_data['shares'] = value
    return equity_data

if __name__ == "__main__":
    json_output_path = 'analysis'
    tickers_file_path = 'scrape_psx/tickers/tickers.json'
    output_dir = 'output/scraped_tickers'
    
    tickers = load_tickers(tickers_file_path)
    symbols = [ticker['symbol'] for ticker in tickers]
    
    available_symbols = [symbol for symbol in symbols if os.path.isfile(os.path.join(output_dir, f"{symbol}.html"))]
    
    scraped_info = []
    for ticker in tickers:
        if ticker['symbol'] in available_symbols:
            file_path = os.path.join(output_dir, f"{ticker['symbol']}.html")
            data = extract_data_from_html(file_path)
            ticker_info = {
                "symbol": ticker['symbol'],
                "name": ticker['name'],
                "sector": ticker['sectorName'],
                "financials": data
            }
            scraped_info.append(ticker_info)
    
    # print(json.dumps(scraped_info, indent=4))
    with open(json_output_path + '/scraped_data.json', 'w') as outfile:
        json.dump(scraped_info, outfile, indent=4)