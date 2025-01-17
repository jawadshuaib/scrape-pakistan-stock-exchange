# PSX Stock Analysis Project

The purpose of this project is to identify companies trading on the Pakistan Stock Exchange below their intrinsic value.

This project scrapes all the stocks listed on the Pakistan Stock Exchange (PSX). It then calculates the growth rate for each company and feeds that into Google Sheets to discover the intrinsic value.

Please note, this project is for educational purposes only. Please refer to guidelines on PSX for the efficacy of scraping data.

## Steps:

1. **Get Tickers:**

   - A list of tickers for all available stocks on the PSX is available at `scrape_psx/tickers/tickers.json`.

2. **Scrape Tickers:**

   - Use Scrapy to scrape the tickers in the `tickers.json`, and store the raw HTML at `output/scraped_tickers`.
   - Command: `scrapy crawl scrape_tickers`

3. **Extract Financial Information:**

   - Use `analysis/extract_from_scraped_pages.py` to extract financial information from the downloaded HTML pages. The data is outputted to a JSON file called `analysis/scraped_data.json`.

   The format of the extracted data looks like this:

   ```json
   {
   	"symbol": "AABS",
   	"name": "Al-Abbas Sugar Mills Limited",
   	"sector": "SUGAR & ALLIED INDUSTRIES",
   	"financials": {
   		"Sales": ["16507771", "14569235", "10362184", "7421377"],
   		"EPS": ["89.31", "212.22", "110.22", "43.31"],
   		"market_cap": "12560408690.0",
   		"shares": "17362300",
   		"price": "723.43"
   	}
   }
   ```

4. **Calculate CAGR:**

   - Calculate the compounded annual growth rates (CAGR) for EPS and Sales to determine the growth rates. The data is stored in a pandas DataFrame and exported as a CSV file.

5. **Google Sheets Integration:**
   - This exported data can then be imported into Google Sheets. For example, the following sheet uses the EPS growth rates to determine the intrinsic value and margin of safety price of each of the stocks trading on the PSX. This allows us to quickly find potentially undervalued companies.

Last updated (January 2025): [Google Sheets Link](https://docs.google.com/spreadsheets/d/1X4-QnntyD_KeImqazNnbKY6xzWuWYCS44ezv3ZQZ_LU/edit?usp=sharing)

The above Google Sheet calculates the intrinsic value and margin of safety price using an API. The API uses discounted cash flow methodology for Earnings per Share (EPS) and growth rate to arrive at fair value.

The script for the API call can be found in stock-valuation-script.gs.
