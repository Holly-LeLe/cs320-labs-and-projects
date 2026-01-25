# Add additional imports if needed

import json
from csv import DictReader
from io import TextIOWrapper
from zipfile import ZipFile

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

with open('banks.json') as f:
    banks = json.load(f)

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()

        # TODO: add each race to self.race using race_lookup
        for r in race:
            continue


    def lower_age(self):
        # TODO: return the lower bound of the applicant’s age range as an int
        pass

    def __lt__(self, other):
        # TODO: return True if this applicant is younger than the other
        pass
    
    def __repr__(self):
        # TODO: return a string like Applicant('25-34', ['White', 'Asian'])
        pass

    def __str__(self):
        return self.__repr__()


class Loan:
    def __init__(self, values):
        # TODO: use float_extract to set loan_amount, property_value, and interest_rate
        self.loan_amount = self.float_extract(values, "loan_amount")
        self.property_value = None
        self.interest_rate = None

        # TODO: create a list of Applicant objects for applicant and co-applicant
        self.applicants = []

    def float_extract(self, values, attr):
        # TODO: return -1.0 if value is "Exempt" or "NA", otherwise return float(val)
        pass

    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0
        assert self.loan_amount > 0

        amt = self.loan_amount

        while amt > 0: 
            # TODO: yield amt
            # TODO: add interest rate multiplied by amt to amt
            # TODO: subtract yearly payment from amt
            break # remove this line once you implement this function

    def __str__(self):
        # TODO: return a summary string like "<Loan: 4.5% on $200000 with 2 applicant(s)>"
        pass

    def __repr__(self):
        return self.__str__()


class Bank:
    def __init__(self, name):
        self.name = name
        self.lei = None
        self.loans = []

        # TODO: look up bank’s LEI in banks.json using `banks`

        # TODO: read wi.zip/wi.csv and load Loan objects belonging to this bank


    def __len__(self):
        # TODO: return the number of loans
        pass

    def __getitem__(self, idx):
        # TODO: return loan at index idx
        pass