import requests
from bs4 import BeautifulSoup

class ConnectionManager:
    def __init__(self, url):
        self.url = url

    def get_connection(self):
        try:
            response = requests.get(self.url)
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