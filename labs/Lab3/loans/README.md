# Loan Module

In these exercises, you'll start writing a `loans.py` module with two
Python classes you'll use for MP3.  It's OK if you don't finish these
classes during lab time (you can finish them with your group or alone
later when working on MP3).

## loans.py

In Jupyter, do the following:
1. Go to MP3
2. Remember to also switch to the `MP3` branch before you begin. If you are still working on another project, save your progress by adding and commiting the files before checking out the new branch. 
3. Open `loans.py`

**Important note on testing:** Throughout this portion on the lab you will be testing your `loans.py` module in a `.ipynb` notebook. You can either test directly in `mp3.ipynb` or create a separate `debug.ipynb` notebook for testing and debugging the module. If you choose to use the `mp3.ipynb` notebook, remember that you can add cells to it, but be careful to not modify the cells that have `#QX` in them as the output of these will be graded for the project. 

Using a `.py` module is easy, just run `import some_mod` to run
`some_mod.py`, loading any functions or classes it has.

Open your notebook and make sure that `import loans` is included at the top (if you are using `mp3.ipynb` this should already be there). 

Add the following two lines as well. They reload the module whenever you make changes to it.

```
%load_ext autoreload
%autoreload 2
```

Note this doesn't work all the time (if there's a bug in your loans.py, you may need to do a Restart & Run All in the notebook after fixing your module).

## 1. `Applicant` class

We'll want to create a class to represent people who apply for loans. Take a look at the starter code for the `Applicant` class.

We'll be using HDMA loan data
(https://www.ffiec.gov/hmda/pdf/2023guide.pdf), which uses numeric
codes to represent race.  Here are the codes from the documentation,
recorded in a dictionary (you can also find them already included at the top of `loans.py`):

```python
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}
```

Use the `race_lookup` dictionary to complete the `__init__` constructor. The loop should add entries in the `race` parameter to the `self.race` attribute of the class, converting from the numeric codes to text in the process.  The `race` attribute is a set because applicants often identify with multiple options.

**Note:**  Assume that the race parameter is either a string of digits or a list of strings of digits.

Simply skip over any entries in the `race` parameter that don't appear in the `race_lookup` dict (e.g., we'll see and skip "6" later because that code indicates a missing value).

Test the code you wrote in `loans.py` from your notebook to make sure the `Applicant.__init__` constructor properly fills the
`race` set.

```python
applicant = loans.Applicant("20-30", ["1", "2", "3"])
applicant.race
```

You should see this set:

```python
{'American Indian or Alaska Native', 'Asian', 'Black or African American'}
```

### `__repr__`

Take a look at the `__repr__` method in your `Applicant` class and complete it.

Putting `applicant` at the end of a cell or printing `repr(applicant)` should show this:

```
Applicant('20-30', ['American Indian or Alaska Native', 'Asian', 'Black or African American'])
```

**Note:** The `race` attribute should be sorted lexicographically. It is also now a list, not a set, in this output.

### `lower_age`

You might notice that ages are given as strings rather than ints
because we need to support ranges (like "20-30").

The `lower_age` method should return the lower int of an applicant's age range.

It should also support ages like "<75" (should just return the int
`75`) and ">25" (should just return the int `25`).

Try your method (you should get the int `20` since the age is "20-30"):

```python
applicant.lower_age()
```

Hints: you could use `.replace` get get rid of unhelpful characters
(like "<" and ">").  After that, splitting on "-" could help you find
the first number (it's OK to split on a character that doesn't appear
in a string, you just get a list with one entry).

### `__lt__`

Recall that `__lt__` ("less than") lets you control what happens when
two objects get compared.

`obj1 < obj2` automatically becomes `obj1.__lt__(obj2)`, so you can
write `__lt__` to return a True/False, indicating whether `obj1` is
less than `obj2`.

Complete the `__lt__` function in the `Applicant` class. 

Comparisons should be based on lower age. (Hint: use lower_age method) Python sorting will also use your `__lt__` method.  Try it:

```python
sorted([
    loans.Applicant(">75", ["43", "44"]),
    loans.Applicant("20-30", ["1", "3"]),
    loans.Applicant("35-44", ["22"]),
    loans.Applicant("<25", ["5"]),
])
```

You should get this order:

```python
[Applicant('20-30', ['American Indian or Alaska Native', 'Black or African American']),
 Applicant('<25', ['White']),
 Applicant('35-44', ['Chinese']),
 Applicant('>75', ['Other Pacific Islander', 'Samoan'])]
```

## 2. `Loan` class

For the project, we'll use data loan data from this site:
https://cfpb.github.io/hmda-platform/#hmda-api-documentation.

Loan applications are described with dictionaries, all with the same keys. The following is an example which you can use for debugging and testing:

```python
values = {'activity_year': '2020', 'lei': '549300FX7K8PTEQUU487', 'derived_msa-md': '31540', 'state_code': 'WI',
         'county_code': '55025', 'census_tract': '55025002402', 'conforming_loan_limit': 'C',
         'derived_loan_product_type': 'Conventional:First Lien',
         'derived_dwelling_category': 'Single Family (1-4 Units):Site-Built',
         'derived_ethnicity': 'Not Hispanic or Latino', 'derived_race': 'White', 'derived_sex': 'Male',
         'action_taken': '3', 'purchaser_type': '0', 'preapproval': '2', 'loan_type': '1', 'loan_purpose': '4',
         'lien_status': '1', 'reverse_mortgage': '2', 'open-end_line_of_credit': '1',
         'business_or_commercial_purpose': '2', 'loan_amount': '225000.0', 'loan_to_value_ratio': '78.671',
         'interest_rate': '3.000', 'rate_spread': 'NA', 'hoepa_status': '3', 'total_loan_costs': 'NA',
         'total_points_and_fees': 'NA', 'origination_charges': 'NA', 'discount_points': 'NA',
         'lender_credits': 'NA', 'loan_term': '360', 'prepayment_penalty_term': 'NA', 'intro_rate_period': '1',
         'negative_amortization': '2', 'interest_only_payment': '2', 'balloon_payment': '2',
         'other_nonamortizing_features': '2', 'property_value': '285000', 'construction_method': '1',
         'occupancy_type': '1', 'manufactured_home_secured_property_type': '3',
         'manufactured_home_land_property_interest': '5', 'total_units': '1', 'multifamily_affordable_units': 'NA',
         'income': '0', 'debt_to_income_ratio': '>60%', 'applicant_credit_score_type': '1',
         'co-applicant_credit_score_type': '10', 'applicant_ethnicity-1': '2', 'applicant_ethnicity-2': '',
         'applicant_ethnicity-3': '', 'applicant_ethnicity-4': '', 'applicant_ethnicity-5': '',
         'co-applicant_ethnicity-1': '5', 'co-applicant_ethnicity-2': '', 'co-applicant_ethnicity-3': '',
         'co-applicant_ethnicity-4': '', 'co-applicant_ethnicity-5': '', 'applicant_ethnicity_observed': '2',
         'co-applicant_ethnicity_observed': '4', 'applicant_race-1': '5', 'applicant_race-2': '',
         'applicant_race-3': '', 'applicant_race-4': '', 'applicant_race-5': '', 'co-applicant_race-1': '8',
         'co-applicant_race-2': '', 'co-applicant_race-3': '', 'co-applicant_race-4': '', 'co-applicant_race-5': '',
         'applicant_race_observed': '2', 'co-applicant_race_observed': '4', 'applicant_sex': '1',
         'co-applicant_sex': '5', 'applicant_sex_observed': '2', 'co-applicant_sex_observed': '4',
         'applicant_age': '55-64', 'co-applicant_age': '9999', 'applicant_age_above_62': 'Yes',
         'co-applicant_age_above_62': 'NA', 'submission_of_application': '1', 'initially_payable_to_institution': '1',
         'aus-1': '6', 'aus-2': '', 'aus-3': '', 'aus-4': '', 'aus-5': '', 'denial_reason-1': '1',
         'denial_reason-2': '', 'denial_reason-3': '', 'denial_reason-4': '', 'tract_population': '3572',
         'tract_minority_population_percent': '41.1499999999999986', 'ffiec_msa_md_median_family_income': '96600',
         'tract_to_msa_income_percentage': '64', 'tract_owner_occupied_units': '812',
         'tract_one_to_four_family_homes': '910', 'tract_median_age_of_housing_units': '45'}
```

Paste the above to your notebook.  We want to use a dict like the above to create a `Loan` object as follows:

```python
loan = loans.Loan(values)
```

Whereas the `__init__` for `Applicant` took a few parameters, the
`__init__` for the `Loan` class takes a single parameter,
`values`, which will contain all the data necessary to set the `Loan`
attributes.

Requirements:
* The `Loan` object should have four attributes: `loan_amount`, `property_value`, `interest_rate`, `applicants`
* The first three attributes are floats, using the `float_extract` method convert a string into a float. If the string is either "NA" or "Exempt" (that represent missing values), `float_extract()` should return -1, otherwise it should extract the float value from the string.
* The `applicants` attribute should be a list of `Applicant` objects, where the minimum number of elements of the list is 1 (applicant) and the maximum number of elements of the list is 2 (applicant and co-applicant).  
* Every loan object has at least one applicant, with age values["applicant_age"] and race(s) in the multiple values["applicant_race-????"] entries.
* Some loans have a second applicant (but no more) -- you'll know there is a second applicant when values["co-applicant_age"] != "9999". In that case, self.applicants should contain two Applicant objects, with the info from the second coming from the values["co-applicant_age"] and values["co-applicant_race-????"] entries.


Manually test your `Loan` class from your notebook with a few snippets:
* `loan.interest_rate` should be `3.0`
* `loan.applicants` should be `[Applicant('55-64', ['White'])]`
* choose a couple more...

### `__str__` and `__repr__`

Complete the `__str__` method in the `Loan` class so that `print(loan)` gives the following:

```
<Loan: 3.0% on $225000.0 with 1 applicant(s)>
```

Take a look at `__repr__`, it returns the same string as `__str__`.

**Note:** your print output should include **all** of the same characters, including the "<" and ">" and everything between.

### `yearly_amounts`

The loans have details regarding payment amount and frequency in the
terms, but for simplicity, we'll ignore that here.

The `yearly_amounts` method in the `Loan` class should be a generator
that yields loan amounts, as the loan is payed off over time.  Assume
that each year, a single payment is made, after interest is
calculated. 

**Note:** `loan.interest_rate` is in percentage. Convert it
to decimal before using it. Failure to do so may result in interest 
that will never be paid off, creating an infinite loop!

Complete the `TODO`s in the `yearly_amounts` function and test in your notebook: 

```python
for amt in loan.yearly_amounts(80000):
    print(amt)
```

You should get the following:

```
225000.0
151750.0
76302.5
```

Make sure the method works as a generator by yielding `amt`. One advantage of the generator is that the method will work even if the payment is too small (the generator will keep yielding larger amounts as the debt keeps growing). 

**This last step is very important to passing the MP tests!**
