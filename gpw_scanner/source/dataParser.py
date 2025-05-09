import re

class DataParser:
    def __init__(self, table_name):
        self.table_name = table_name

    def table_finder(self, soup):
        table = soup.find("table", self.table_name)
        rows = table.find_all("tr")
        return rows

    def fetch_chosen_income(self,rows, income_name):
        counter = 0
        incomes = []
        for row in rows:
            if income_name in row.text:
                values = [td.get_text(strip=True) for td in row.find_all("td")]
                for value in values:
                    incomes.append(value)
                counter += 1
                break
        return incomes

    def fetch_report_years(self, rows):
        years = []
        for row in rows:
            headers = [th.get_text(strip=True) for th in row.find_all("th")]
            if headers:
                for header in headers:
                    match = re.match(r"(\d{4})", header)
                    if match:
                        year = match.group(1)
                        years.append(year)
        return years