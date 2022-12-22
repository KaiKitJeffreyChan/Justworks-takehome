import pandas as pd

def get_data(file_name):
    xl_file = pd.ExcelFile(file_name)
    dfs = {}
    for sheet_name in xl_file.sheet_names:
        dfs[sheet_name] = xl_file.parse(sheet_name)
    return dfs

pages = get_data('test.xlsx')