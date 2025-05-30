class Company:
    def __init__(self, ticker, name, share_price, income_revenue_collection, income_gross_profit_collection, income_EBIT_collection, income_net_profit_collection, share_amount):
        self.name = name
        self.ticker = ticker
        self.share_price = share_price
        self.income_revenue = income_revenue_collection
        self.income_gross_profit = income_gross_profit_collection
        self.income_EBIT = income_EBIT_collection
        self.income_net_profit_collection = income_net_profit_collection
        self.share_amount = share_amount

    def display_info(self):
        print(self.name)
        print(self.ticker)
        print(self.income_revenue)
        print(self.income_gross_profit)
        print(self.income_EBIT)
        print(self.income_net_profit_collection)
