class RankPosition:
    def __init__(self, points, company_name, company_ticker, share_price, eps, pe, avr_pe, yearly_income_revenues, yearly_income_revenues_industry, yearly_income_gross_profit, yearly_income_gross_profit_industry, yearly_income_EBIT, yearly_income_EBIT_industry, yearly_income_net_profit, yearly_income_net_profit_industry, no_negative_income_revenues_ratio, constantly_income_revenues_increase):
        self.points = points
        self.company_name = company_name
        self.company_ticker = company_ticker
        self.share_price = share_price
        self.eps = eps
        self.pe = pe
        self.avr_pe = avr_pe
        self.yearly_income_revenues = yearly_income_revenues
        self.yearly_income_revenues_industry = yearly_income_revenues_industry
        self.yearly_income_gross_profit = yearly_income_gross_profit
        self.yearly_income_gross_profit_industry = yearly_income_gross_profit_industry
        self.yearly_income_EBIT = yearly_income_EBIT
        self.yearly_income_EBIT_industry = yearly_income_EBIT_industry
        self.yearly_income_net_profit = yearly_income_net_profit
        self.yearly_income_net_profit_industry = yearly_income_net_profit_industry
        self.no_negative_income_revenues_ratio = no_negative_income_revenues_ratio
        self.constantly_income_revenues_increase = constantly_income_revenues_increase
