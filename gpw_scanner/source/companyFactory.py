from selenium.webdriver.chrome.service import Service
from source.company import Company
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.financialData import IncomeGrossProfit, IncomeNetProfit
from source.financialData import IncomeEBIT
from source.incomeFactory import IncomeFactory


class CompanyFactory:
    def __init__(self):
        pass

#ToDO
#In create_company_collection:
#1)Extract all financial data into separetly method()
#2)Add data from wskaniki table
    def create_company_collection(self, company_ticker_collection, company_name_collection):
        Company_collection = []
        count = 0 #temporary solution for restrict amount of company
        service = Service('C:\\chromium-browser\\chromedriver.exe')
        for company_ticker in company_ticker_collection:
            if count < 3 :

                financial_report_url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_ticker},Q"
                financial_connection = SeleniumConnectionManager(financial_report_url, service)
                financial_data_soup = financial_connection.get_soup_for_chosen_indicator(financial_connection, service,)
                financial_parser = DataParser("report-table")
                financial_rows = financial_parser.rows_table_finder(financial_data_soup)
                income_revenues = financial_parser.fetch_chosen_income(financial_rows, "Przychody ze sprzedaży") #ToDO consider try/catch that can help return the company with wrong stats(example bank)
                income_gross_profit = financial_parser.fetch_chosen_income(financial_rows, "Zysk ze sprzedaży")
                income_EBIT = financial_parser.fetch_chosen_income(financial_rows, "Zysk operacyjny (EBIT)")
                income_net_profit = financial_parser.fetch_chosen_income(financial_rows, "Zysk netto")
                years_collection = financial_parser.fetch_report_years(financial_rows)
                new_income = IncomeFactory()
                income_revenues_collection = new_income.create_income_collection(income_revenues, years_collection)
                income_gross_profit_collection = new_income.create_income_collection(income_gross_profit, years_collection,                                                          IncomeGrossProfit)
                income_EBIT_collection = new_income.create_income_collection(income_EBIT, years_collection, IncomeEBIT)
                income_net_profit_collection = new_income.create_income_collection(income_net_profit, years_collection, IncomeNetProfit)
                share_price = financial_parser.get_share_price(financial_data_soup)

                #data gathering place

                indicator_report_url = f"https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/{company_ticker},Q"
                indicator_connection = SeleniumConnectionManager(indicator_report_url, service)
                indicator_data_soup = indicator_connection.get_soup_for_chosen_indicator(indicator_connection, service)
                indicator_parser = DataParser("report-table")
                share_amount = indicator_parser.get_newest_share_amount(indicator_data_soup)

                new_company = f"{company_ticker}"
                new_company = Company(company_ticker, company_name_collection[count] , share_price, income_revenues_collection,
                                  income_gross_profit_collection, income_EBIT_collection, income_net_profit_collection, share_amount)
                Company_collection.append(new_company)
                count += 1

        return Company_collection