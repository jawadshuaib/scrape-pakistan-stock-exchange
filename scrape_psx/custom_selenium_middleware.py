# custom_selenium_middleware.py
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class CustomSeleniumMiddleware:
    def __init__(self, *args, **kwargs):
        # Initialize Chrome options
        chrome_options = Options()
        chrome_options.binary_location = settings.get('SELENIUM_DRIVER_BINARY_LOCATION')
        for arg in settings.get('SELENIUM_DRIVER_ARGUMENTS'):
            chrome_options.add_argument(arg)

        # Use Service to specify ChromeDriver path
        service = Service(settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH'))

        # Set up the WebDriver with Service and Options
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = str.encode(self.driver.page_source)
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def __del__(self):
        self.driver.quit()
