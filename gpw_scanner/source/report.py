
from source.rankPosition import RankPosition

class Report:
    def __init__(self):
        pass

    def normalize_number(self, value: str) -> float:
        value = value.lstrip('+')
        return float(value)

    def get_score(self, income_data, weight):
        score = income_data * weight
        return score

    def calculate_score(self, value, weight):
        if value is not None:
            try:
                converted = self.normalize_number(value)
                return self.get_score(converted, weight)
            except Exception:
                return 0  # Optionally log the error
        return 0

    def get_report(self, company_collection):
        ranking = []
        for company in company_collection:
            scoring = 0
            income_revenues_r_r = company.income_revenue[-1].r_to_r
            income_gross_profit_r_r = company.income_gross_profit[-1].r_to_r
            income_EBIT_r_r = company.income_EBIT[-1].r_to_r
            income_net_profit_r_r = company.income_net_profit[-1].r_to_r
            revenue_score = self.calculate_score(income_revenues_r_r, 0.2)
            gross_score = self.calculate_score(income_gross_profit_r_r, 0.2)
            ebit_score = self.calculate_score(income_EBIT_r_r, 0.3)
            net_score = self.calculate_score(income_net_profit_r_r, 0.3)


            scoring += revenue_score + gross_score + ebit_score + net_score
            new_entity = RankPosition(format(scoring, '.2f'), company.name, company.ticker, income_revenues_r_r,
                                      income_gross_profit_r_r, income_EBIT_r_r, income_net_profit_r_r,)
            ranking.append(new_entity)
        return ranking