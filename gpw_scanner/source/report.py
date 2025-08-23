from datetime import date
import csv

from numpy.ma.extras import average
from selenium.webdriver.common.devtools.v134.accessibility import query_ax_tree

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
        eps = int(income_net_profit) * 1000  / int(share_amount)
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

        for value in collection[-num_of_quartals:]:
            # Ensure the value is a string and replace comma with dot
            cleaned_value = str(value).replace(",", ".")
            try:
                total += float(cleaned_value)
            except ValueError:
                print(f"Skipping invalid value: {value}")
                continue

        avg = total / num_of_quartals
        return avg

    def calculate_non_negative_ratio(self, collection):
        total = len(collection)
        non_negative_count = sum(1 for x in collection if x >= 0)
        ratio = (non_negative_count / total) * 100
        return f"{ratio}%"

    def last_years_all_income_revenue_positive(self, collection, quartals):
        if len(collection) < quartals:
            return False
        return all(x >= 0 for x in collection[-quartals:])

    #Todo consider to remove
    def calculate_constantly_income_increase(self, collection, years):
        print(f"Full input collection: {collection}")

        if len(collection) < 10:
            print("The collection has fewer than 10 elements.")
            return False

        last_10 = collection[-10:]
        print(f"Last 10 elements: {last_10}")

        for i in range(9):
            print(f"Comparing: {last_10[i]} < {last_10[i + 1]}")
            if last_10[i] >= last_10[i + 1]:
                print(f"Failed at index {i}: {last_10[i]} is not less than {last_10[i + 1]}")
                return False

        print("Last 10 elements are strictly increasing.")
        return True

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
          #  for income in company.income_revenue_collection:
           #     print(income)
            share_price = company.share_price
            yearly_income_revenues = company.income_revenue_collection[-1].yearly_growth_pct
            yearly_income_revenues_industry = company.income_revenue_collection[-1].yearly_growth_Industry_pct
          #  for income in company.income_revenue_collection:
           #     print(income.yearly_growth_Industry_pct)


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


            price_to_earnings_ratio_avr = self.calculate_avg_value(price_to_earnings_collection, 20)

            income_net_collection = []
            for net in company.income_net_profit_collection:
                income_net_collection.append(net.income)

            quarterly_sum_of_net_profit = self.calculate_income(income_net_collection, -4)
            eps = self.calculate_EPS(quarterly_sum_of_net_profit, share_amount)

            if price_to_earnings_collection:
                pe = price_to_earnings_collection[-1]
            else:
                pe = None

            if pe == 0 or pe is None:
                pe = self.calculate_PE(share_price, eps)


            temp_income_revenues_collection = []
            for element in company.income_revenue_collection:
                temp_income_revenues_collection.append(float(element.yearly_growth_pct))

            no_negative_income_revenues_ratio = self.calculate_non_negative_ratio(temp_income_revenues_collection)
            constantly_income_revenues_increase = self.last_years_all_income_revenue_positive(temp_income_revenues_collection, 40)
            revenue_score = self.calculate_score(yearly_income_revenues)
            gross_score = self.calculate_score(yearly_income_gross_profit)
            ebit_score = self.calculate_score(yearly_income_EBIT)
            net_score = self.calculate_score(yearly_income_net_profit,)
            if revenue_score > 0 and gross_score > 0 and ebit_score > 0 and yearly_income_EBIT and net_score >0:
                scoring += revenue_score + gross_score + ebit_score + net_score + 50
            else:
                scoring += revenue_score + gross_score + ebit_score + net_score
            new_entity = RankPosition(format(scoring, '.2f'), company.name, company.ticker, share_price, eps, pe, price_to_earnings_ratio_avr, f"{yearly_income_revenues}%", f"{yearly_income_revenues_industry}%",
                                      f"{yearly_income_gross_profit}%", f"{yearly_income_gross_profit_industry}%", f"{yearly_income_EBIT}%", f"{yearly_income_EBIT_industry}%", f"{yearly_income_net_profit}%", f"{yearly_income_net_profit_industry}%", no_negative_income_revenues_ratio, constantly_income_revenues_increase)
            ranking.append(new_entity)
        return ranking

    def export_to_csv(self, ranking):
        report_date = date.today()
        sorted_ranking =sorted(ranking, key=lambda rank: float(rank.points), reverse=True)
        file = open(f"C:\\gpw_scanner\\gpw_scanner\\resources\\gpw_report_{report_date}.csv", mode="w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=["Points", "Company", "Ticker", "Cena akcji", "Zysk na akcje(EPS)", "Cena do Zysku(PE)","Srednia wartosc Cena do Zysku dla 5-ciu lat", "Przychody ze sprzedazy [%] r/r", "Przychody ze sprzedazy branza [%] r/r",
                                                      "Zysk ze sprzedazy [%] r/r","Zysk ze sprzedazy branza [%] r/r" , "Zysk operacyjny [%] (EBIT)", "Zysk operacyjny branza [%] (EBIT)", "Zysk Netto [%]", "Zysk Netto branza [%]", "Liczba kwartalow z nieujemnymi przychodami", "Nieprzerwanie dodatnie przychody przez ostatnie 10 lat"])
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
                "Zysk Netto branza [%]": rank.yearly_income_net_profit_industry,
                "Liczba kwartalow z nieujemnymi przychodami": rank.no_negative_income_revenues_ratio,
                "Nieprzerwanie dodatnie przychody przez ostatnie 10 lat": rank.constantly_income_revenues_increase

            })
        print("The cvs report was successfully created!")
