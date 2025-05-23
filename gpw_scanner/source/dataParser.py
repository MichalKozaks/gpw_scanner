import re

class DataParser:
    def __init__(self, table_name):
        self.table_name = table_name

    def rows_table_finder(self, soup):
        table = soup.find("table", self.table_name)
        rows = table.find_all("tr")
        return rows

    def table_finder(self, soup):
        table = soup.find("table", {'class': f'{self.table_name}'})
        return table

    def fetch_chosen_income(self,rows, income_name):
        counter = 0
        incomes = []
        for row in rows:
            if income_name in row.text:
                values = [td.get_text(strip=True) for td in row.find_all("td")]
                for value in values:
                    if income_name not in value:
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

    def fetch_company_information(self, stock_table):
        if stock_table is None:
            print("Error: No table found")
        else:
            company_names_collection = []
            ticker_collection = []

            for row in stock_table.find_all('tr')[1:]:  # skip the header row
                columns = row.find_all('td')
                if columns:
                    company_name = columns[0].text.strip()
                    link = columns[0].find('a')
                    title = link['title'].strip().upper()
                    match = re.match(r'^(\w+)\s*\((\w+)\)', company_name)
                    if "BANK" in title or "MBANK" in title or "GETIN" in title or "SANTANDER" in title or "UNICREDIT" in title:  #Exclude bank sector because have other financial stats. We need to do this here because create_company_collection() require pure list of company - any try catch have no sense there ... because new company instance will have wrong parse date that lead to wrong stats for company
                        continue
                    if match:
                        ticker = match.group(1).strip()
                        name = match.group(2).strip()
                        ticker_collection.append(ticker)
                        company_names_collection.append(name)
            return company_names_collection, ticker_collection