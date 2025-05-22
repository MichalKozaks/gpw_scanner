class RankPosition:
    def __init__(self, points, company_name, company_ticker, income_revenues_r_r, income_gross_profit_r_r, income_EBIT_r_r, income_net_profit_r_r):
        self.points = points
        self.company_name = company_name
        self.company_ticker = company_ticker
        self.income_revenues_r_r = income_revenues_r_r
        #ToDO self.income_revenues_r_r_industry = income_revenues_r_r_industry -need to be added in a future
        self.income_gross_profit_r_r = income_gross_profit_r_r
        # self.income_gross_profit_r_r_industry = income_gross_profit_r_r_industry -need to be added in a future
        self.income_EBIT_r_r = income_EBIT_r_r
        self.income_net_profit_r_r = income_net_profit_r_r
