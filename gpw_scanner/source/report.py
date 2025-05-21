
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

    def get_report(self, company_collection):
        ranking = []
        for company in company_collection:
            all_scores = 0
            income_revenues_r_r = company.income_revenue[-1].r_to_r
            income_gross_profit_r_r = company.income_gross_profit[-1].r_to_r
            if income_revenues_r_r and income_revenues_r_r is not None:
                income_revenue_converted = self.normalize_number(income_revenues_r_r)
                score = self.get_score(income_revenue_converted, 0.5)
            else:
                score = 0
            if income_gross_profit_r_r and income_gross_profit_r_r is not None:
                income_gross_profit_converted = self.normalize_number(income_gross_profit_r_r)
                score2 = self.get_score(income_gross_profit_converted, 0.5)
            else:
                score2 = 0

            all_scores += score + score2
            new_entity = RankPosition(all_scores, company.name, company.ticker, income_revenues_r_r,
                                      income_gross_profit_r_r)
            ranking.append(new_entity)
        return ranking