from source.connectionManager import ConnectionManager
from source.dataParser import DataParser
from source.companyFactory import CompanyFactory
from source.report import Report
import time

start_time = time.time()
stock_url = "https://www.biznesradar.pl/gielda/akcje_gpw"
stock_connection = ConnectionManager(stock_url)
stock_soup = stock_connection.get_connection()

print("Analyse has been started")
stock_parser = DataParser("table table--accent-header table--accent-first table--even table--nowrap table--sticky-first-col table--sticky-header")
stock_table = stock_parser.table_finder(stock_soup)

company_name_collection , company_ticker_collection = stock_parser.fetch_company_information(stock_table)

CompanyFactory = CompanyFactory()
Company_collection = CompanyFactory.create_company_collection(company_name_collection, company_ticker_collection)

ranking = Report()
ranking.export_to_csv(ranking.get_report(Company_collection))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
