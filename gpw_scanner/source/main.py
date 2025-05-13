from selenium.webdriver.chrome.service import Service

from source.company import Company
from source.SeleniumConnectionManager import SeleniumConnectionManager
from source.dataParser import DataParser
from source.fdata import IncomeGrossProfit
from source.incomeFabric import IncomeFabric

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


#### Working fine section for INCOME
company_name = company_name_collection[0]
company_url = f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{company_name}"
print(company_url)
service = Service('C:\\chromium-browser\\chromedriver.exe')
SeleniumConnection = SeleniumConnectionManager(company_url, service)
driver = SeleniumConnection.start_selenium_connection()
soup = SeleniumConnection.start_parse(driver)
#create a Parser
parser = DataParser("report-table")
rows = parser.rows_table_finder(soup)

IncomeRevenuesData = parser.fetch_chosen_income(rows, "Przychody ze sprzedaży")
IncomeGrossProfitData = parser.fetch_chosen_income(rows, "Zysk ze sprzedaży")
Years = parser.fetch_report_years(rows)
new_income = IncomeFabric()
Income_revenues_collection = new_income.create_income_collection(IncomeRevenuesData, Years)
Income_Gross_Profit_collection = new_income.create_income_collection(IncomeGrossProfitData, Years, IncomeGrossProfit)

#Company creation test
#ToDO - some fabirc needed
CompanyNo1 = Company(company_name_collection[0] , company_ticker_collection[0], Income_revenues_collection, Income_Gross_Profit_collection)

all_income = 0
for income in CompanyNo1.income_revenue:
    all_income += income.income
    print(f" {income.id_year}, {income.income}, {income.r_to_r}, {income.r_to_r_industry}") ## ToDo: verify the results seem to be incomplete

#Przydatny githaab do sprawdzenia:
#https://github.com/lebinho/biznesradar/blob/main/biznesradar_stock_analysis.ipynb

#ToDO
#Bardzo podstawowa funkcjonalność:
#1)dokonać operacji (obliczenie sredniej przychodów liczba i % w wybranym okresie (5 lub 10 lub wiecej lat)


