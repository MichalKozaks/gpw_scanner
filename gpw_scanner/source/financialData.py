
class FinancialData:
    def __init__(self, id_year, f_data, year_to_year, year_to_year_trade):
        self.id_year = id_year
        self.f_data = f_data
        self.year_to_year = year_to_year
        self.year_to_year_trade = year_to_year_trade

#Przychody za sprzedazy
class IncomeRevenues(FinancialData):
    def __init__(self, id_year, income, r_to_r, r_to_r_industry):
        super().__init__(id_year, income, r_to_r, r_to_r_industry)
        self.income = income
        self.r_to_r = r_to_r
        self.r_to_r_industry = r_to_r_industry

#Zysk ze sprzedaży
class IncomeGrossProfit(FinancialData):
    def __init__(self, id_year, income, r_to_r, r_to_r_industry):
        super().__init__(id_year, income, r_to_r, r_to_r_industry)
        self.income = income
        self.r_to_r = r_to_r
        self.r_to_r_industry = r_to_r_industry

#Zysk operacyjny (EBIT)
class IncomeEBIT(FinancialData):
    def __init__(self, id_year, income, r_to_r, r_to_r_industry):
        super().__init__(id_year, income, r_to_r, r_to_r_industry)
        self.income = income
        self.r_to_r = r_to_r
        self.r_to_r_industry = r_to_r_industry

#Zysk Netto
class IncomeNetProfit(FinancialData):
    def __init__(self, id_year, income, r_to_r, r_to_r_industry):
        super().__init__(id_year, income, r_to_r, r_to_r_industry)
        self.income = income
        self.r_to_r = r_to_r
        self.r_to_r_industry = r_to_r_industry