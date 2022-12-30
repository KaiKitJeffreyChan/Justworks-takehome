import pandas as pd
import pprint

# get data from xlsx file, filtered empty rows and grouped by users
def get_transactions(filename):
  all_user_data = {}
  df = pd.read_excel(filename, sheet_name="Data")
  for index, row in df.iterrows():
    if(pd.isnull(row['Customer Id']) == False):
      # if user is not in all_user_data, add user to all_user_data
      if(row['Customer Id'] not in all_user_data):
        # separate credit and debit transactions for each user
        if(row['Amount'] > 0):
          all_user_data[row['Customer Id']] = {
            "credit": [],
            "debit": [[row['Date'], row['Amount']]],
          }
        else:
          all_user_data[row['Customer Id']] = {
            "credit": [[row['Date'], row['Amount']]],
            "debit": [],
          }
      else:
        if(row['Amount'] > 0):
          all_user_data[row['Customer Id']]['debit'].append([row['Date'], row['Amount']])
        else:
          all_user_data[row['Customer Id']]['credit'].append([row['Date'], row['Amount']])     
  return all_user_data


# compare Timestamp of two transactions 
def get_time_comparison(time1, time2):
  if(time1 == time2):
    time_comparison = "equal"
  else:
    time_comparison = time1 < time2
  return time_comparison
    
# adds transaction details to user_balance 
def add_balance(user_balances, user, transaction):
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

def generate_balances(all_user_data):
  user_balances = {}
  finish_credit_transactions, finish_debit_transactions = False, False
  for user in all_user_data:
    user_balances[user] = {}
    credit_transactions = all_user_data[user]['credit']
    debit_transactions = all_user_data[user]['debit']
    credit_ptr, debit_ptr = 0, 0
    exit_loop = False
    while (credit_ptr < len(credit_transactions) or debit_ptr < len(debit_transactions)):
      if(exit_loop):
        break
      time_comparison = get_time_comparison(credit_transactions[credit_ptr][0], debit_transactions[debit_ptr][0])
      
      #if time_comparison is true, then credit transaction is applied first
      #if time_comparison is false, then debit transaction is applied first
      #if time_comparison is equal, then both transactions are applied but credit first then debit
      if(time_comparison == True):
        while(time_comparison == True):
          add_balance(user_balances, user, credit_transactions[credit_ptr])
          #if credit_ptr is at the end of the credit_transactions, then exit loop and finish debit transactions
          if(credit_ptr == (len(credit_transactions) - 1)):
            finish_debit_transactions = True
            exit_loop = True
            break
          credit_ptr += 1
          time_comparison = get_time_comparison(credit_transactions[credit_ptr][0], debit_transactions[debit_ptr][0])
      elif(time_comparison == False):
        while(time_comparison == False):
          add_balance(user_balances, user, debit_transactions[debit_ptr])
          #if debit_ptr is at the end of the debit_transactions, then exit loop and finish credit transactions
          if(debit_ptr == (len(debit_transactions) - 1)):
            exit_loop = True
            finish_credit_transactions = True
            break
          debit_ptr += 1
          time_comparison = get_time_comparison(credit_transactions[credit_ptr][0], debit_transactions[debit_ptr][0])
      elif(time_comparison == "equal"):
        while(time_comparison == "equal"):
          add_balance(user_balances, user, credit_transactions[credit_ptr])
          add_balance(user_balances, user, debit_transactions[debit_ptr])
          # if credit_ptr or debit_ptr is at the end of the credit_transactions or debit_transactions, then exit loop and finish credit or debit transactions
          if(debit_ptr == (len(debit_transactions) - 1)):
            exit_loop = True
            finish_credit_transactions = True
            break
          elif(credit_ptr == (len(credit_transactions) - 1)):
            finish_debit_transactions = True
            exit_loop = True
            break
          credit_ptr += 1
          debit_ptr += 1
          time_comparison = get_time_comparison(credit_transactions[credit_ptr][0], debit_transactions[debit_ptr][0])
          
    #if there are still transactions left in either credit or debit, add them to the user_balances
    if(finish_credit_transactions):
      while(credit_ptr < len(credit_transactions)):
        add_balance(user_balances, user, credit_transactions[credit_ptr])
        credit_ptr += 1
    elif(finish_debit_transactions):
      while(debit_ptr < len(debit_transactions)):
        add_balance(user_balances, user, debit_transactions[debit_ptr])
        debit_ptr += 1
        
  return user_balances


all_user_data = get_transactions("Intern-AccountTransactions.xlsx")
pprint.pprint(generate_balances(all_user_data))