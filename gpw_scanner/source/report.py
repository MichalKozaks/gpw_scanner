from datetime import date
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

    def calculate_income(self, income_collection, number_of_quarters):
        temp_income_collection = income_collection[number_of_quarters:]
        sum_of_income = 0
        for income in temp_income_collection:
            sum_of_income += int(income)
        return sum_of_income

    def calculate_EPS(self, income_net_profit, share_amount ):
        eps = float(income_net_profit) * 1000 / float(share_amount)
        return eps

    def calculate_PE(self, share_price, eps):
        pe = share_price/eps
        return pe

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
            share_price = company.share_price
            income_revenues_r_r = company.income_revenue[-1].r_to_r
            income_revenues_r_to_r_industry = company.income_revenue[-1].r_to_r_industry
            income_gross_profit_r_r = company.income_gross_profit[-1].r_to_r
            income_gross_profit_r_r_industry = company.income_gross_profit[-1].r_to_r_industry
            income_EBIT_r_r = company.income_EBIT[-1].r_to_r
            income_EBIT_r_r_industry = company.income_EBIT[-1].r_to_r_industry
            income_net_profit_r_r = company.income_net_profit_collection[-1].r_to_r
            income_net_profit_r_r_industry = company.income_net_profit_collection[-1].r_to_r_industry
            share_amount = int(company.share_amount.replace(" ", ""))
            income_net_collection = []
            for net in company.income_net_profit_collection:
                income_net_collection.append(net.income)

            quarterly_sum_of_net_profit = self.calculate_income(income_net_collection, -4)
            eps = self.calculate_EPS(quarterly_sum_of_net_profit, share_amount)
            pe = self.calculate_PE(share_price, eps)

            revenue_score = self.calculate_score(income_revenues_r_r)
            gross_score = self.calculate_score(income_gross_profit_r_r)
            ebit_score = self.calculate_score(income_EBIT_r_r)
            net_score = self.calculate_score(income_net_profit_r_r,)
            if revenue_score > 0 and gross_score > 0 and ebit_score > 0 and income_EBIT_r_r and net_score >0:
                scoring += revenue_score + gross_score + ebit_score + net_score + 50
            else:
                scoring += revenue_score + gross_score + ebit_score + net_score
            new_entity = RankPosition(format(scoring, '.2f'), company.name, company.ticker, share_price, eps, pe, income_revenues_r_r, income_revenues_r_to_r_industry,
                                      income_gross_profit_r_r, income_gross_profit_r_r_industry, income_EBIT_r_r, income_EBIT_r_r_industry, income_net_profit_r_r, income_net_profit_r_r_industry)
            ranking.append(new_entity)
        return ranking

    def export_to_csv(self, ranking):
        report_date = date.today()
        sorted_ranking =sorted(ranking, key=lambda rank: float(rank.points), reverse=True)
        file = open(f"C:\\gpw_scanner\\gpw_scanner\\resources\\gpw_report_{report_date}.csv", mode="w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=["Points", "Company", "Ticker", "Cena akcji", "Zysk na akcje(EPS)", "Cena do Zysku(PE)", "Przychody ze sprzedazy r/r", "Przychody ze sprzedazy branza r/r",
                                                      "Zysk ze sprzedazy r/r","Zysk ze sprzedazy branza r/r" , "Zysk operacyjny (EBIT)", "Zysk operacyjny branza (EBIT)", "Zysk Netto", "Zysk Netto branza"])
        writer.writeheader()
        for rank in sorted_ranking:
            writer.writerow({
                "Points": rank.points,
                "Company": rank.company_name,
                "Ticker": rank.company_ticker,
                "Cena akcji": rank.share_price,
                "Zysk na akcje(EPS)": rank.eps,
                "Cena do Zysku(PE)": rank.pe,
                "Przychody ze sprzedazy r/r": rank.income_revenues_r_r,
                "Przychody ze sprzedazy branza r/r": rank.income_revenues_r_to_r_industry,
                "Zysk ze sprzedazy r/r": rank.income_gross_profit_r_r,
                "Zysk ze sprzedazy branza r/r": rank.income_gross_profit_r_to_r_industry,
                "Zysk operacyjny (EBIT)": rank.income_EBIT_r_r,
                "Zysk operacyjny branza (EBIT)": rank.income_EBIT_r_r_industry,
                "Zysk Netto": rank.income_net_profit_r_r,
                "Zysk Netto branza": rank.income_net_profit_r_r_industry

            })
        print("The cvs report was successfully created!")
