import re

from source.financialData import IncomeRevenues

class IncomeFactory:
    def __init__(self):
        pass

    def create_income_collection(self, incomes, years, cls = IncomeRevenues):
        counter = 0
        income_collection = []
        pattern = re.compile(
            r'(?P<value>[+-]?\d{1,3}(?:\s\d{3})?)'  
            r'(?:r/r(?P<rr>[+-]?\d+\.\d+)%~branża(?P<branza1>[+-]?\d+\.\d+))?'
        )
        for income in incomes:
            match = pattern.search(income)
            if match:
                new_income = f"income_{years[counter]}"
                year_income = match.group("value").replace(" ", "")
                r_to_r  = match.group("rr") if match.group("rr") else 0
                r_to_r_industry  = match.group("branza1") if match.group("branza1") else 0
                new_income = cls(years[counter], year_income, r_to_r , r_to_r_industry )
                income_collection.append(new_income)
                counter += 1
        return income_collection


