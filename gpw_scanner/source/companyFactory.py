from selenium.webdriver.chrome.service import Service

from source.company import Company
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.fdata import IncomeGrossProfit, IncomeNetProfit
from source.fdata import IncomeEBIT
from source.incomeFactory import IncomeFactory


class CompanyFactory:
    def __init__(self):
        pass

    def create_company_collection(self, company_ticker_collection, company_name_collection):
        Company_collection = []
        count = 0 #temporary solution for restrict amount of company
        for company_ticker in company_ticker_collection:
            if count < 6:
                company_url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_ticker},Q"
                service = Service('C:\\chromium-browser\\chromedriver.exe')
                selenium_connection = SeleniumConnectionManager(company_url, service)
                driver = selenium_connection.start_selenium_connection()
                soup = selenium_connection.start_parse(driver)
                # create a Parser
                parser = DataParser("report-table")
                rows = parser.rows_table_finder(soup)
                income_revenues = parser.fetch_chosen_income(rows, "Przychody ze sprzedaży")
                income_gross_profit = parser.fetch_chosen_income(rows, "Zysk ze sprzedaży")
                income_EBIT = parser.fetch_chosen_income(rows, "Zysk operacyjny (EBIT)")
                income_net_profit = parser.fetch_chosen_income(rows, "Zysk netto")
                years_collection = parser.fetch_report_years(rows)
                new_income = IncomeFactory()
                income_revenues_collection = new_income.create_income_collection(income_revenues, years_collection)
                income_gross_profit_collection = new_income.create_income_collection(income_gross_profit, years_collection,
                                                                                 IncomeGrossProfit)
                income_EBIT_collection = new_income.create_income_collection(income_EBIT, years_collection, IncomeEBIT)
                income_net_profit_collection = new_income.create_income_collection(income_net_profit, years_collection, IncomeNetProfit)
                new_company = f"{company_ticker}"
                new_company = Company(company_ticker, company_name_collection[count], income_revenues_collection,
                                  income_gross_profit_collection, income_EBIT_collection, income_net_profit_collection)
                Company_collection.append(new_company)
                count += 1

        return Company_collection