from datetime import date
import csv

from numpy.ma.extras import average

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

    def calculate_avg_value(self, collection, num_of_quartals):
        total = 0
        number_of_elements = len(collection)

        if number_of_elements == 0 or number_of_elements < 20:
            print("Not enough data to calculate average value")
            return 0
#ToDo: safe for company that hasn't 20 quarterrs in idicators history!
        for value in collection[-num_of_quartals:]:
            total += int(value)

        #avg = total / number_of_elements
        avg = total / num_of_quartals

        return avg

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
            yearly_income_revenues = company.income_revenue[-1].yearly_growth_pct
            yearly_income_revenues_industry = company.income_revenue[-1].yearly_growth_Industry_pct
            yearly_income_gross_profit = company.income_gross_profit[-1].yearly_growth_pct
            yearly_income_gross_profit_industry = company.income_gross_profit[-1].yearly_growth_Industry_pct
            yearly_income_EBIT = company.income_EBIT[-1].yearly_growth_pct
            yearly_income_EBIT_industry = company.income_EBIT[-1].yearly_growth_Industry_pct
            yearly_income_net_profit = company.income_net_profit_collection[-1].yearly_growth_pct
            yearly_income_net_profit_industry = company.income_net_profit_collection[-1].yearly_growth_Industry_pct
            share_amount = int(company.share_amount.replace(" ", ""))
            price_to_earnings_collection = []
            for pe in company.price_to_earnings_collection:
                price_to_earnings_collection.append(pe.income)
             #   print(pe.income)

            price_to_earnings_ratio_avr = self.calculate_avg_value(price_to_earnings_collection, 20)

            income_net_collection = []
            for net in company.income_net_profit_collection:
                income_net_collection.append(net.income)

            quarterly_sum_of_net_profit = self.calculate_income(income_net_collection, -4)
            eps = self.calculate_EPS(quarterly_sum_of_net_profit, share_amount)
            pe = self.calculate_PE(share_price, eps)

            revenue_score = self.calculate_score(yearly_income_revenues)
            gross_score = self.calculate_score(yearly_income_gross_profit)
            ebit_score = self.calculate_score(yearly_income_EBIT)
            net_score = self.calculate_score(yearly_income_net_profit,)
            if revenue_score > 0 and gross_score > 0 and ebit_score > 0 and yearly_income_EBIT and net_score >0:
                scoring += revenue_score + gross_score + ebit_score + net_score + 50
            else:
                scoring += revenue_score + gross_score + ebit_score + net_score
            new_entity = RankPosition(format(scoring, '.2f'), company.name, company.ticker, share_price, eps, pe, price_to_earnings_ratio_avr, yearly_income_revenues, yearly_income_revenues_industry,
                                      yearly_income_gross_profit, yearly_income_gross_profit_industry, yearly_income_EBIT, yearly_income_EBIT_industry, yearly_income_net_profit, yearly_income_net_profit_industry)
            ranking.append(new_entity)
        return ranking

    def export_to_csv(self, ranking):
        report_date = date.today()
        sorted_ranking =sorted(ranking, key=lambda rank: float(rank.points), reverse=True)
        file = open(f"C:\\gpw_scanner\\gpw_scanner\\resources\\gpw_report_{report_date}.csv", mode="w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=["Points", "Company", "Ticker", "Cena akcji", "Zysk na akcje(EPS)", "Cena do Zysku(PE)","Srednia wartosc Cena do Zysku dla 5-ciu lat", "Przychody ze sprzedazy [%] r/r", "Przychody ze sprzedazy branza [%] r/r",
                                                      "Zysk ze sprzedazy [%] r/r","Zysk ze sprzedazy branza [%] r/r" , "Zysk operacyjny [%] (EBIT)", "Zysk operacyjny branza [%] (EBIT)", "Zysk Netto [%]", "Zysk Netto branza [%]"])
        writer.writeheader()
        for rank in sorted_ranking:
            writer.writerow({
                "Points": rank.points,
                "Company": rank.company_name,
                "Ticker": rank.company_ticker,
                "Cena akcji": rank.share_price,
                "Zysk na akcje(EPS)": rank.eps,
                "Cena do Zysku(PE)": rank.pe,
                "Srednia wartosc Cena do Zysku dla 5-ciu lat": rank.avr_pe,
                "Przychody ze sprzedazy [%] r/r": rank.yearly_income_revenues,
                "Przychody ze sprzedazy branza [%] r/r": rank.yearly_income_revenues_industry,
                "Zysk ze sprzedazy [%] r/r": rank.yearly_income_gross_profit,
                "Zysk ze sprzedazy branza [%] r/r": rank.yearly_income_gross_profit_industry,
                "Zysk operacyjny [%] (EBIT)": rank.yearly_income_EBIT,
                "Zysk operacyjny branza [%] (EBIT)": rank.yearly_income_EBIT_industry,
                "Zysk Netto [%]": rank.yearly_income_net_profit,
                "Zysk Netto branza [%]": rank.yearly_income_net_profit_industry

            })
        print("The cvs report was successfully created!")
