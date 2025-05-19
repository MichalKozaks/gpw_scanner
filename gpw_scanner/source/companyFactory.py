from source.company import Company
from selenium.webdriver.chrome.service import Service

from source.company import Company
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.fdata import IncomeGrossProfit
from source.incomeFactory import IncomeFactory


class CompanyFactory:
    def __init__(self):
        pass

    def create_company_collection(self, company_ticker_collection, company_name_collection):
        Company_collection = []
        count = 0 #temporary solution for restrict amount of company
        for company_ticker in company_ticker_collection:
            if count < 3:
                company_url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_ticker},Q"
                service = Service('C:\\chromium-browser\\chromedriver.exe')
                selenium_connection = SeleniumConnectionManager(company_url, service)
                driver = selenium_connection.start_selenium_connection()
                soup = selenium_connection.start_parse(driver)
                # create a Parser
                parser = DataParser("report-table")
                rows = parser.rows_table_finder(soup)

                income_revenues_data = parser.fetch_chosen_income(rows, "Przychody ze sprzedaży")
                income_gross_profit_data = parser.fetch_chosen_income(rows, "Zysk ze sprzedaży")
                years_collection = parser.fetch_report_years(rows)
                new_income = IncomeFactory()
                income_revenues_collection = new_income.create_income_collection(income_revenues_data, years_collection)
                income_gross_profit_collection = new_income.create_income_collection(income_gross_profit_data, years_collection,
                                                                                 IncomeGrossProfit)
                new_company = f"{company_ticker}"
                new_company = Company(company_ticker, company_name_collection[count], income_revenues_collection,
                                  income_gross_profit_collection)
                Company_collection.append(new_company)
                count += 1

        return Company_collection