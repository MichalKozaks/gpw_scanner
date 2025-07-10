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

    def get_share_price(self, soup):
        price_span = soup.find('span', class_='q_ch_act')
        share_price = float(price_span.text) if price_span else None
        return share_price

    def get_newest_share_amount(self, soup):
        share_amount_row = soup.find('tr', attrs={'data-field': 'ShareAmount'})
        value_cell = share_amount_row.find('td', class_='h newest') if share_amount_row else None
        share_amount = value_cell.find('span', class_='pv').find('span').text if value_cell else None
        return share_amount

    def get_CZ_values(self, soup):
        share_amount_row = soup.find('tr', attrs={'data-field': 'CZ'})
        value_cell = share_amount_row.find('td', class_='h newest') if share_amount_row else None
        share_amount = value_cell.find('span', class_='pv').find('span').text if value_cell else None
        return share_amount

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
                    if any(bank in title for bank in ["BANK", "MBANK", "GETIN", "SANTANDER", "UNICREDIT"]): #Exclude bank sector because have other financial stats. We need to do this here because create_company_collection() require pure list of company - any try catch have no sense there ... because new company instance will have wrong parse date that lead to wrong stats for company
                        continue

                    match = re.match(r'^(\w+)\s*\((\w+)\)', company_name)
                    if match:
                        ticker = match.group(1).strip()
                        name = match.group(2).strip()
                    else:
                        # "XXX" company names pattern
                        ticker = company_name
                        name = company_name

                    ticker_collection.append(ticker)
                    company_names_collection.append(name)
            return company_names_collection, ticker_collection