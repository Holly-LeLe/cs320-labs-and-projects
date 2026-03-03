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
        if isinstance(race, str):
            race_iter = [race]
        else:
            race_iter = race

        for r in race_iter:
            if r in race_lookup:
                self.race.add(race_lookup[r])


    def lower_age(self):
        # TODO: return the lower bound of the applicant’s age range as an int
        s = self.age.replace("<", "").replace(">", "")
        first = s.split("-")[0]
        return int(first)

    def __lt__(self, other):
        # TODO: return True if this applicant is younger than the other
        return self.lower_age() < other.lower_age()
    
    def __repr__(self):
        # TODO: return a string like Applicant('25-34', ['White', 'Asian'])
        races_sorted = sorted(self.race)
        return f"Applicant({self.age!r}, {races_sorted})"

    def __str__(self):
        return self.__repr__()


class Loan:
    def __init__(self, values):
        # TODO: use float_extract to set loan_amount, property_value, and interest_rate
        self.loan_amount = self.float_extract(values, "loan_amount")
        self.property_value = self.float_extract(values, "property_value")
        self.interest_rate = self.float_extract(values, "interest_rate")

        # TODO: create a list of Applicant objects for applicant and co-applicant
        self.applicants = []
        def collect_races(prefix): 
            races = [] 
            for i in range(1, 6): 
                key = f"{prefix}{i}" 
                if key in values and values[key] != "": 
                    races.append(values[key]) 
            return races

        
        app_age = values["applicant_age"]
        app_races = collect_races("applicant_race-")
        self.applicants.append(Applicant(app_age, app_races))

        if values["co-applicant_age"] != "9999":
            co_age = values["co-applicant_age"]
            co_races = collect_races("co-applicant_race-")
            self.applicants.append(Applicant(co_age, co_races))

    def float_extract(self, values, attr):
        # TODO: return -1.0 if value is "Exempt" or "NA", otherwise return float(val)
        val = values[attr]
        if val == "Exempt" or val == "NA":
            return -1.0
        else:
            return float(val)

    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0
        assert self.loan_amount > 0

        amt = self.loan_amount
        rate = self.interest_rate / 100.0

        while amt > 0: 
            # TODO: yield amt
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            amt += amt * rate
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment


    def __str__(self):
        # TODO: return a summary string like "<Loan: 4.5% on $200000 with 2 applicant(s)>"
        return f"<Loan: {self.interest_rate:.1f}% on ${self.loan_amount:.1f} with {len(self.applicants)} applicant(s)>"

    def __repr__(self):
        return self.__str__()


class Bank:
    def __init__(self, name):
        self.name = name
        self.lei = None
        self.loans = []

        # TODO: look up bank’s LEI in banks.json using `banks`
        if isinstance(banks, dict):
            # most common: {"Bank Name": "LEI", ...}
            if name in banks:
                self.lei = banks[name]
            else:
                lowered = {k.lower(): v for k, v in banks.items()}
                if name.lower() in lowered:
                    self.lei = lowered[name.lower()]
                else:
                    raise KeyError(f"Bank name not found in banks.json: {name}")
        elif isinstance(banks, list):
            for item in banks:
                if item.get("name") == name:
                    self.lei = item.get("lei")
                    break
            if self.lei is None:
                raise KeyError(f"Bank name not found in banks.json: {name}")
        else:
            raise TypeError("banks must be a dict or a list (loaded from banks.json).")
            
         # TODO: read wi.zip/wi.csv and load Loan objects belonging to this bank
        with ZipFile("wi.zip") as z:
            with z.open("wi.csv") as raw:
                f = TextIOWrapper(raw, encoding="utf-8")
                reader = DictReader(f)
                for values in reader:
                    # each row is a dict; keep only rows for this bank's LEI
                    if values.get("lei") == self.lei:
                        self.loans.append(Loan(values))

    def __len__(self):
        # TODO: return the number of loans
        return len(self.loans)

    def __getitem__(self, idx):
        # TODO: return loan at index idx
        return self.loans[idx]