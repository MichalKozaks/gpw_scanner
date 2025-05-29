class Company:
    def __init__(self, ticker, name, share_price, income_revenue, income_gross_profit, income_EBIT, income_net_profit, share_amount):
        self.name = name
        self.ticker = ticker
        self.share_price = share_price
        self.income_revenue = income_revenue
        self.income_gross_profit = income_gross_profit
        self.income_EBIT = income_EBIT
        self.income_net_profit = income_net_profit
        self.share_amount = share_amount


    def display_info(self):
        print(self.name)
        print(self.ticker)
        print(self.income_revenue)
        print(self.income_gross_profit)
        print(self.income_EBIT)
        print(self.income_net_profit)
