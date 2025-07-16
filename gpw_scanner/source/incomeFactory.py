import re

from source.financialData import IncomeRevenues

class IncomeFactory:
    def __init__(self):
        pass

    def create_income_collection(self, incomes, years, cls=IncomeRevenues):
        income_collection = []
        pattern = re.compile(
            r'(?P<value>[+-]?\d{1,3}(?:\s\d{3})?)'
            r'(?:r/r(?P<rr>[+-]?\d+\.\d+)%~branża(?P<branza1>[+-]?\d+\.\d+))?'
        )

        for i in range(min(len(incomes), len(years))):
            income = incomes[i]
            match = pattern.search(income) if income else None

            if match:
                year_income = match.group("value").replace(" ", "")
                r_to_r = match.group("rr") if match.group("rr") else 0
                r_to_r_industry = match.group("branza1") if match.group("branza1") else 0
            else:
                year_income = 0
                r_to_r = 0
                r_to_r_industry = 0

            new_income = cls(years[i], year_income, r_to_r, r_to_r_industry)
            income_collection.append(new_income)

        return income_collection



