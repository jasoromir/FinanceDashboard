
import pandas as pd
from constants import dict_names

def get_data(ticker):
    # Get general info
    info_sheet = ticker.info

    # Get balance sheet
    balance_sheet = ticker.balance_sheet

    # Fetch the income statement data
    income_statement = ticker.financials

    last_date = str(balance_sheet.columns[0].date())

    dict_values = {}
    for name, keyword in dict_names.items():
        if keyword in list(balance_sheet.index):
            value = balance_sheet.loc[keyword, last_date]
        elif keyword in list(income_statement.index):
            value = income_statement.loc[keyword, last_date]
        elif keyword in list(info_sheet.keys()):
            value = info_sheet[keyword]
        elif name == 'Growth Rate':
            eps_forward = info_sheet['forwardEps']
            eps_current = info_sheet['trailingEps']
            value = (eps_forward/eps_current-1)*100
        else:
            value = dict_names[name]
        dict_values[name] = value

    df = pd.DataFrame(dict_values.items(), columns = ['fields', 'values'])

    return df