# How to run the following program ----------------------------------------------------------------

# Method 1: 
# Go to https://replit.com/join/vyluvgtidb-jeffreychan6 and login with the following credentials
# Username: Justworks
# Password: Justworks
# Press the Green Run button and view the console output (on the right side of the screen)

# Method 2: 
# In the current dir, run $ pip install pandas 
# Then run python3 calculate_balances.py 

# Method 3: 
# Go to https://github.com/KaiKitJeffreyChan/Justworks-takehome and follow the instructions in the README.md

# Assumptions ---------------------------------------------------------------------------------------

#All credit transactions were (-) and all debit transactions were (+)
#All transactions will be in order (ex. a transaction on Dec 12th 2022 could not be followed by a transaction on Dec 5th 2022)
#There could be multiple transactions within the same day
#There could be an uneven amount of debit and credit transactions
#There could be multiple months for a single user

import pandas as pd
import pprint

# class to hold transaction data
class Transaction:
  def __init__(self, customer_id, date, amount):
    self.customer_id = customer_id
    self.date = date
    self.amount = amount
  
  def __str__(self):
    return "Date: " + str(self.date) + " Amount: " + str(self.amount)
  
  def __repr__(self):
    return "Date: " + str(self.date) + " Amount: " + str(self.amount)

# get data from xlsx file, filtered empty rows and grouped by users
def get_transactions(filename):
  all_user_data = {}
  df = pd.read_excel(filename, sheet_name="Data")
  for index, row in df.iterrows():
    if(pd.isnull(row['Customer Id']) == False):
      new_transaction = Transaction(row["Customer Id"], row['Date'], row['Amount'])
      # if user is not in all_user_data, add user to all_user_data
      if(new_transaction.customer_id not in all_user_data):
        all_user_data[new_transaction.customer_id] = {}
      # if date is not in all_user_data[user], add date to all_user_data[user]
      if(new_transaction.date not in all_user_data[new_transaction.customer_id]):
        all_user_data[new_transaction.customer_id][new_transaction.date] = []
      # add transaction to all_user_data[user][date]
      all_user_data[new_transaction.customer_id][new_transaction.date].append(new_transaction)

  # sort all transactions by value so we can calculate credit transactions first
  for user in all_user_data:
    for date in all_user_data[user]:
      all_user_data[user][date].sort(key=lambda x: x.amount)
          
  pprint.pprint(all_user_data)
  return all_user_data
    
# adds transaction details to user_balance 
def add_balance(user_balances, transaction):
  date = transaction.date
  amount = transaction.amount
  user = transaction.customer_id
  month = date.strftime("%B")
  year = date.strftime("%Y")
  month_year = month + "/" + year
  if(month_year not in user_balances[user]):
    user_balances[user][month_year] = {
      "min": amount,
      "max": amount,
      "end": amount,
    }
  else:
    user_balances[user][month_year]["end"] += amount
    if(user_balances[user][month_year]["min"] > user_balances[user][month_year]["end"]):
      user_balances[user][month_year]["min"] = user_balances[user][month_year]["end"]
    if(user_balances[user][month_year]["max"] < user_balances[user][month_year]["end"]):
      user_balances[user][month_year]["max"] = user_balances[user][month_year]["end"]

def generate_balances(all_user_data):
  user_balances = {}
  # add all transactions to user_balances
  for user in all_user_data:
    user_balances[user] = {}
    for date in all_user_data[user]:
      for transaction in all_user_data[user][date]:
        add_balance(user_balances, transaction)
        
  return user_balances


all_user_data = get_transactions("Intern-AccountTransactions.xlsx")
pprint.pprint(generate_balances(all_user_data))
