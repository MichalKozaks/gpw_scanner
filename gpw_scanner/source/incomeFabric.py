import re
from source.fdata import IncomeRevenues

class IncomeFabric:
    def __init__(self):
        pass

    def create_income_collection(self, incomes, years, cls = IncomeRevenues):
        counter = 1  # for this moment is 1(read from second year)
        income_collection = []
        for income in incomes:
            # Regular expression to extract value and two percentages
            match = re.match(r"([\d\s]+)r/r([+-]?\d+\.\d+)%~branża([+-]?\d+\.\d+)%", income)
            if match:
                new_income = f"income_{years[counter]}"
                income = match.group(1).strip()
                int_income = int(income.replace(",", "").replace(" ", ""))
                r_to_r = match.group(2)
                r_to_r_industry = match.group(3)
                new_income = cls(years[counter], int_income, r_to_r, r_to_r_industry)
                income_collection.append(new_income)
                counter += 1
                # TODO
                # Fix counter = 0 (first row has null for: income, r_to_r, r_to_r_industry

        return income_collection