import pandas as pd
import csv

from source.rankPosition import RankPosition

class Report:
    def __init__(self):
        pass
    #ToDO - consider use try/catch
    def normalize_number(self, value: str) -> float:
        value = value.lstrip('+')
        return float(value)

    def get_score(self, income_data, weight):
        score = income_data * weight
        return score

    def calculate_score(self, value):
        if value is not None:
            try:
                converted = self.normalize_number(value)
                if 0 < converted <= 50:
                    return 10
                elif 50 < converted <= 100:
                    return 20
                elif converted > 100:
                    return 30
                elif -50 < converted < 0:
                    return -30
                elif -100 < converted <= -50:
                    return -50
                elif -200 < converted <= -100:
                    return -100
                elif converted <= -200:
                    return -150
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
            revenue_score = self.calculate_score(income_revenues_r_r)
            gross_score = self.calculate_score(income_gross_profit_r_r)
            ebit_score = self.calculate_score(income_EBIT_r_r)
            net_score = self.calculate_score(income_net_profit_r_r,)
            if revenue_score > 0 and gross_score > 0 and ebit_score > 0 and income_EBIT_r_r and net_score >0:
                scoring += revenue_score + gross_score + ebit_score + net_score + 50
                print("+50 bonus for all positive stats")
            else:
                scoring += revenue_score + gross_score + ebit_score + net_score
            new_entity = RankPosition(format(scoring, '.2f'), company.name, company.ticker, income_revenues_r_r,
                                      income_gross_profit_r_r, income_EBIT_r_r, income_net_profit_r_r,)
            ranking.append(new_entity)
        return ranking

    def export_to_csv(self, ranking):
        sorted_ranking =sorted(ranking, key=lambda rank: float(rank.points), reverse=True)
        file = open("C:\\gpw_scanner\\gpw_scanner\\resources\\gpw_report.csv", mode="w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=["Points", "Company", "Ticker", "Przychody ze sprzedazy r/r",
                                                      "Zysk ze sprzedaży r/r", "Zysk operacyjny (EBIT)", "Zysk Netto"])
        writer.writeheader()
        for rank in sorted_ranking:
            print(f"Points: {rank.points} Company: {rank.company_name} Ticker: {rank.company_ticker} Przychody ze sprzedaży r/r: {rank.income_revenues_r_r} Zysk ze sprzedaży r/r {rank.income_gross_profit_r_r} Zysk operacyjny (EBIT): {rank.income_EBIT_r_r} Zysk Netto: {rank.income_net_profit_r_r} ")
            writer.writerow({
                "Points": rank.points,
                "Company": rank.company_name,
                "Ticker": rank.company_ticker,
                "Przychody ze sprzedazy r/r": rank.income_revenues_r_r,
                "Zysk ze sprzedaży r/r": rank.income_gross_profit_r_r,
                "Zysk operacyjny (EBIT)": rank.income_EBIT_r_r,
                "Zysk Netto": rank.income_net_profit_r_r
            })
        print("The cvs report is prepared with successfully !")
