
class FinancialData:
    def __init__(self, id_year, financial_data, yearly_growth_pct, yearly_growth_Industry_pct):
        self.id_year = id_year
        self.financial_data = financial_data
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct
#Przychody za sprzedazy
class IncomeRevenues(FinancialData):
    def __init__(self, id_year, income, yearly_growth_pct, yearly_growth_Industry_pct):
        super().__init__(id_year, income, yearly_growth_pct, yearly_growth_Industry_pct)
        self.income = income
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct
#Zysk ze sprzedaży
class IncomeGrossProfit(FinancialData):
    def __init__(self, id_year, income, yearly_growth_pct, yearly_growth_Industry_pct):
        super().__init__(id_year, income, yearly_growth_pct, yearly_growth_Industry_pct)
        self.income = income
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct
#Zysk operacyjny (EBIT)
class IncomeEBIT(FinancialData):
    def __init__(self, id_year, income, yearly_growth_pct, yearly_growth_Industry_pct):
        super().__init__(id_year, income, yearly_growth_pct, yearly_growth_Industry_pct)
        self.income = income
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct
#Zysk Netto
class IncomeNetProfit(FinancialData):
    def __init__(self, id_year, income, yearly_growth_pct, yearly_growth_Industry_pct):
        super().__init__(id_year, income, yearly_growth_pct, yearly_growth_Industry_pct)
        self.income = income
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct

class PriceToEarningsRatio(FinancialData):
    def __init__(self, id_year, income, yearly_growth_pct, yearly_growth_Industry_pct):
        super().__init__(id_year, income, yearly_growth_pct, yearly_growth_Industry_pct)
        self.income = income
        self.yearly_growth_pct = yearly_growth_pct
        self.yearly_growth_Industry_pct = yearly_growth_Industry_pct