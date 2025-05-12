from selenium.webdriver.chrome.service import Service

from source.conManager import ConnectionManager
from source.dataParser import DataParser
from source.fdata import IncomeGrossProfit
from source.incomeFabric import IncomeFabric

url = "https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/ORLEN"
#Q -kwartalne
#Y -roczne
#C -skumulowane

service = Service('C:\\chromium-browser\\chromedriver.exe')
connection = ConnectionManager(url, service)
driver = connection.start_selenium_connection()
soup = connection.start_parse(driver)
#create a Parser
parser = DataParser("report-table")
rows = parser.table_finder(soup)

IncomeRevenuesData = parser.fetch_chosen_income(rows, "Przychody ze sprzedaży")
IncomeGrossProfitData = parser.fetch_chosen_income(rows, "Zysk ze sprzedaży")
Years = parser.fetch_report_years(rows)
new_income = IncomeFabric()
Income_revenues_collection = new_income.create_income_collection(IncomeRevenuesData, Years)
Income_Gross_Profit_collection = new_income.create_income_collection(IncomeGrossProfitData, Years, IncomeGrossProfit)

all_income = 0
for income in Income_Gross_Profit_collection:
    all_income += income.income
    print(f" {income.id_year}, {income.income}, {income.r_to_r}, {income.r_to_r_industry}")

print("Sum of income: ", all_income)

#Przydatny githaab do sprawdzenia:
#https://github.com/lebinho/biznesradar/blob/main/biznesradar_stock_analysis.ipynb

#ToDO
#Bardzo podstawowa funkcjonalność:
#1)zrobic generator klasy ftype z danych
#2)Stworzyc kolekcje danych
#3)dokonać operacji (obliczenie sredniej przychodów liczba i % w wybranym okresie (5 lub 10 lub wiecej lat)


