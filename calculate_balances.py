#Problem:

#Justworks wants to generate insight from a list of banking 
# transactions occurring in customer accounts. We want to generate 
# minimum , maximum and ending balances by month for customers. 
# You can assume starting balance at begining of month is 0.
# You should read transaction data from csv files and produce 
# output in the format mentioned below. 

#Please apply credit transactions first to calculate balance 
# on a given day.  Please write clear instructions on how to run 
# your program on a local machine. Please use dataset in Data Tab 
# to test your program.

#Input CSV Format:
#CustomerID, Date, Amount, Credit/Debit

#Output Format:
#CustomerID, MM/YYYY, Min Balance, Max Balance, Ending Balance

import pandas as pd
import pprint

#get data from xlsx file, filtered empty rows and grouped by users
def get_transactions(filename):
  all_user_data = {}
  df = pd.read_excel(filename, sheet_name="Data")
  for index, row in df.iterrows():
    #need to check for credit/debit!!!
    if(pd.isnull(row['Customer Id']) == False):
      if(row['Customer Id'] not in all_user_data):
        all_user_data[row['Customer Id']] = [[row['Date'], row['Amount']]]
      else:
        all_user_data[row['Customer Id']].append([row['Date'], row['Amount']])
  return all_user_data
    
def generate_balances(all_user_data):
  user_balances = {}
  for user in all_user_data:
    user_balances[user] = {}
    for transaction in all_user_data[user]:
      date = transaction[0]
      amount = transaction[1]
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
  pprint.pprint(user_balances)
    

  
all_user_data = get_transactions("Intern-AccountTransactions.xlsx")

generate_balances(all_user_data)