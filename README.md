# Justworks-takehome

## How to run the project ##
1. Clone the following repository
2. You can now add your test case xlsx file with the test sheet named "Data" and name it "Intern-AccountTransactions.xlsx", or use the one provided in the email which is already in the repo
3. Run <code>pip install pandas</code>
4. Run <code>python3 calculate_balances.py</code>

## Assumptions ##
* Python3 and pip>=19.3 is installed and there is a working Python virtual environment (if you need to set one up, https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3)
* All credit transactions were (-) and all debit transactions were (+)
* All transactions will be in order (ex. a transaction on Dec 12th could not be followed by a transaction on Dec 5th)
* There could be multiple transactions within the same day
* There could be an uneven amount of debit and credit transactions 
* There could be multiple months for a single user
