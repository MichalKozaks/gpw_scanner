import requests
from bs4 import BeautifulSoup
from source.company import Company
from source.connectionManager import ConnectionManager
from source.dataParser import DataParser
from source.financialData import IncomeGrossProfit, IncomeNetProfit
from source.financialData import IncomeEBIT
from source.incomeFactory import IncomeFactory

class CompanyFactory:
    def __init__(self):
        pass

    def create_company_collection(self, company_ticker_collection, company_name_collection):
        company_collection = []
        count = 0 #temporary solution for restrict amount of company
        for company_ticker in company_ticker_collection:
           # if count < 5 :
                financial_report_url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_ticker},Q"
                #New url explanation
                #Getting new url for is required because financial report url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_ticker},Q"
                #not allowed to get quarterly data, to url adress need be fetched again and modify in way that can properly parse html for quarterly financial results

                headers = {'User-Agent': 'Mozilla/5.0'}  # important for some sites to avoid blocking
                response = requests.get(financial_report_url, headers=headers)
                new_url = ""
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                new_url = f"{response.url},Q"
                financial_connection = ConnectionManager(new_url)
                financial_data_soup = financial_connection.get_connection()
                financial_parser = DataParser("report-table")
                financial_rows = financial_parser.rows_table_finder(financial_data_soup)

                income_revenues = financial_parser.fetch_chosen_income(financial_rows, "Przychody ze sprzedaży") #ToDO consider try/catch that can help return the company with wrong stats(example bank)
                income_gross_profit = financial_parser.fetch_chosen_income(financial_rows, "Zysk ze sprzedaży")
                income_EBIT = financial_parser.fetch_chosen_income(financial_rows, "Zysk operacyjny (EBIT)")
                income_net_profit = financial_parser.fetch_chosen_income(financial_rows, "Zysk netto")
                years_collection = financial_parser.fetch_report_years(financial_rows)
                new_income = IncomeFactory()
                income_revenues_collection = new_income.create_income_collection(income_revenues, years_collection)
                income_gross_profit_collection = new_income.create_income_collection(income_gross_profit, years_collection, IncomeGrossProfit)
                income_EBIT_collection = new_income.create_income_collection(income_EBIT, years_collection, IncomeEBIT)
                income_net_profit_collection = new_income.create_income_collection(income_net_profit, years_collection, IncomeNetProfit)
                share_price = financial_parser.get_share_price(financial_data_soup)

                indicator_report_url = f"https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/{company_ticker},Q"
                indicator_connection = ConnectionManager(indicator_report_url)
                indicator_soup = indicator_connection.get_connection()
                indicator_parser = DataParser("report-table")
                share_amount = indicator_parser.get_newest_share_amount(indicator_soup)

                new_company = f"{company_ticker}"
                new_company = Company(company_ticker, company_name_collection[count] , share_price, income_revenues_collection,
                                  income_gross_profit_collection, income_EBIT_collection, income_net_profit_collection, share_amount)
                company_collection.append(new_company)
                count += 1

        return company_collection