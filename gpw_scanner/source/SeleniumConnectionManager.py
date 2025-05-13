from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class SeleniumConnectionManager:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path

    def start_selenium_connection(self):
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        service = Service(driver_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)
        time.sleep(3) #time to load a page
        return driver

    def end_selenium_connection(self, webdriver):
        webdriver.quit()

    def start_parse(self, webdriver):
        soup = BeautifulSoup(webdriver.page_source, 'html.parser')
        webdriver.quit()
        return soup

