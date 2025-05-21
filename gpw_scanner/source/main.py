from traceback import print_tb
from selenium.webdriver.chrome.service import Service
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.companyFactory import CompanyFactory
from source.report import Report

stock_url = "https://www.biznesradar.pl/gielda/akcje_gpw"
service = Service('C:\\chromium-browser\\chromedriver.exe')
SeleniumConnection = SeleniumConnectionManager(stock_url, service)
driver = SeleniumConnection.start_selenium_connection()
soup = SeleniumConnection.start_parse(driver)

stock_parser = DataParser("table table--accent-header table--accent-first table--even table--nowrap table--sticky-first-col table--sticky-header")
stock_table = stock_parser.table_finder(soup)

company_name_collection , company_ticker_collection = stock_parser.fetch_company_information(stock_table)

CompanyFactory = CompanyFactory()
Company_collection = CompanyFactory.create_company_collection(company_ticker_collection, company_name_collection)

ranking = Report()
ranking.get_report(Company_collection)
ranking = sorted(ranking.get_report(Company_collection), key=lambda rank: rank.points)
print("Sorted collection number of element:", len(ranking))
for rank in ranking:
   print(f"Points: {rank.points} Company: {rank.company_name} Ticker: {rank.company_ticker} Income r/r: {rank.income_revenues_r_r} Income gross r/r {rank.income_gross_profit_r_r}")