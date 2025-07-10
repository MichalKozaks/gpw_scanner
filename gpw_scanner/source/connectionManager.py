import time
import random

import requests
from bs4 import BeautifulSoup

class ConnectionManager:
    def __init__(self, url):
        self.url = url

    def get_connection(self):
        time.sleep(random.uniform(1, 6))
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                return soup
            else:
                print("Connection failed with status code:", response.status_code)
                return None

        except requests.RequestException as e:
            print("An error occurred:", e)
            return None