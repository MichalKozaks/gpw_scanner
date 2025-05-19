from selenium.webdriver.chrome.service import Service

from source.company import Company
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.fdata import IncomeGrossProfit
from source.incomeFactory import IncomeFactory
from source.companyFactory import CompanyFactory


#1.Pobrać liste spólek z gpw jako kolekcja (osobna klasa jakś fetcher)
#2.Na podstawie listy tworzyć poszczegolne obiekty company(Na początek 3 pierwsze spolki/obiekty company)
#3.Sucess -stworzyc mechanizm serializacji company do db(json)
#4.Posegregować/Xrtefaktorować poprzednie kroki pobierania/tworzenia spółek jako sekcja update
#5.Stowrzyć pierwsze kroki ratingu(pracy ma danych) w powiazaniu z jsonem/ a nie bezposrednio z danymi pobieranymi z serwisu
#6.Dalsze rozszerzenie ilośći danych itp.(praca nad resztą parametrów typu przychod)
#7.Kiedyś dodanie wskaznikow

stock_url = "https://www.biznesradar.pl/gielda/akcje_gpw"
#Q -kwartalne
#Y -roczne
#C -skumulowane

service = Service('C:\\chromium-browser\\chromedriver.exe')
SeleniumConnection = SeleniumConnectionManager(stock_url, service)
driver = SeleniumConnection.start_selenium_connection()
soup = SeleniumConnection.start_parse(driver)

stock_parser = DataParser("table table--accent-header table--accent-first table--even table--nowrap table--sticky-first-col table--sticky-header")
stock_table = stock_parser.table_finder(soup)

company_name_collection , company_ticker_collection = stock_parser.fetch_company_information(stock_table)

CompanyFactory = CompanyFactory()
Company_collection = CompanyFactory.create_company_collection(company_ticker_collection, company_name_collection)

print(len(Company_collection))
#check if company list is fulfilled!
for com in Company_collection:
   print(f"{com.name}")
   print(f"{com.ticker}")
   for income in com.income_revenue:
      print(f"data: {income.id_year} {income.income} {income.r_to_r} {income.r_to_r_industry}")


#https://github.com/lebinho/biznesradar/blob/main/biznesradar_stock_analysis.ipynb
