"""
This script defines a Scrapy spider for scraping ticker information from the Pakistan Stock Exchange. The steps involved are:

1. Initialize the spider with necessary configurations and settings.
2. Define the output directory for saving scraped data.
3. Initialize the TickerLoader to manage ticker information and build URLs for scraping.
4. Set up Selenium WebDriver with Chrome options for rendering JavaScript content.
5. Define methods to initialize and close the WebDriver.
6. Implement the parse method to:
   a. Open the target URL using Selenium WebDriver.
   b. Wait for the financial table to be visible.
   c. Extract the page source and save it to an HTML file in the output directory.
   d. Handle any exceptions that occur during the scraping process.

The script outputs HTML files containing the scraped data for each ticker.
"""
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.utils.project import get_project_settings
import os
import json

settings = get_project_settings()
base_url = 'https://dps.psx.com.pk/company/'

class TickerLoader:
    def __init__(self, ticker_file_path, output_dir, skip_duplicates=True):
        self.ticker_file_path = ticker_file_path
        self.output_dir = output_dir
        self.skip_duplicates = skip_duplicates
        self.tickers = self.load_tickers()

    def load_tickers(self):
        with open(self.ticker_file_path) as f:
            tickers = json.load(f)
        if self.skip_duplicates:
            tickers = [ticker for ticker in tickers if not os.path.exists(os.path.join(self.output_dir, f"{ticker['symbol']}.html"))]
        return tickers

    def build_urls(self):
        return [base_url + ticker['symbol'] for ticker in self.tickers]

class TickerSpider(scrapy.Spider):
    name = "scrape_tickers"
    
    def __init__(self, *args, **kwargs):
        super(TickerSpider, self).__init__(*args, **kwargs)
        
        # Define the output directory
        self.output_dir = os.path.join('output', 'scraped_tickers')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize TickerLoader
        ticker_file_path = os.path.join(os.path.dirname(__file__), '..', 'tickers', 'tickers.json')
        self.skip_duplicates = kwargs.get('skip_duplicates', True)
        self.ticker_loader = TickerLoader(ticker_file_path, self.output_dir, self.skip_duplicates)
        # print ('---------------TEST-----------')
        # print (self.ticker_loader.tickers)
        # return
        # Set start_urls
        self.start_urls = self.ticker_loader.build_urls()
        
        # Initialize Chrome options
        self.chrome_options = Options()
        self.chrome_options.binary_location = settings.get('SELENIUM_DRIVER_BINARY_LOCATION')
        for arg in settings.get('SELENIUM_DRIVER_ARGUMENTS'):
            self.chrome_options.add_argument(arg)
        
        # Use Service for specifying the ChromeDriver path
        self.chrome_service = Service(settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH'))
        self.driver = None

    def _init_driver(self):
        self.driver = webdriver.Chrome(service=self.chrome_service, options=self.chrome_options)

    def _close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def parse(self, response):
        self._init_driver()
        self.driver.get(response.url)

        try:
            # Wait for the table to be visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#financialTab .tabs__panel--selected .tbl__wrapper table.tbl'))
            )

            # Extract the page source
            page_source = self.driver.page_source

            # Extract the ticker from the URL
            ticker = response.url.split('/')[-1]

            # Define the file path
            file_path = os.path.join(self.output_dir, f"{ticker}.html")

            # Save the page source to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page_source)

        except Exception as e:
            self.logger.error(f"An error occurred while fetching data from {response.url}: {e}")

        self._close_driver()