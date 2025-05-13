class Company:
    def __init__(self, name, ticker, income_revenue, income_gross_profit):
        self.name = name
        self.ticker = ticker
        self.income_revenue = income_revenue
        self.income_gross_profit = income_gross_profit

    def display_info(self):
        print(self.name)
        print(self.ticker)
        print(self.income_revenue)
        print(self.income_gross_profit)
