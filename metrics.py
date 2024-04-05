import numpy as np
from constants import measure



# DFC per X years
def get_dfc(df, years):
    """ """
    eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]
    growth_rate = df.loc[df.fields == 'Growth Rate', 'values'].values[0]
    pe_rate = df.loc[df.fields == 'P/E (T12M)', 'values'].values[0]
    drr = df.loc[df.fields == 'Desired Rate of Return', 'values'].values[0]/100

    dfc = [eps*(1+growth_rate/100)**i for i in range(0,years)]
    estimated_after = dfc[-1]*pe_rate
    expectStock = [estimated_after/((1+drr)**i) for i in range(0,years)]
    return expectStock[-1]


# GRAHAM NUMBER
def get_graham_number(df):
    total_assests = df.loc[df.fields == 'Total Assets', 'values'].values[0]
    total_liab = df.loc[df.fields == 'Total Liabilities', 'values'].values[0]
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]
    eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]
    
    bvps = (total_assests-total_liab)/num_shares
    fair_value = np.sqrt(measure*eps*bvps)
    return fair_value


# GRAHAMM GROWTH
def get_graham_growth(df):
    try:
        eeg = df.loc[df.fields == 'Growth Rate', 'values'].values[0]/100
        eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]
        drr = df.loc[df.fields == 'Desired Rate of Return', 'values'].values[0]/100
    except Exception as e:
        print(e)

    fair_value = eps*(8.5+2*eeg/(1+drr))
    return fair_value


# BUFFET RATIO
def get_buffet_ratio(df):
    stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]
    ebitda = df.loc[df.fields == 'EBITDA', 'values'].values[0]

    fair_value = stock_price*num_shares/ebitda
    return fair_value


# ROE
def get_roe(df):
    net_income = df.loc[df.fields == 'Net Income', 'values'].values[0]
    total_equity = df.loc[df.fields == 'Total Equity', 'values'].values[0]

    fair_value = net_income/total_equity
    return fair_value


# Munger Multiple
def get_munger_multiplier(df):
    total_assests = df.loc[df.fields == 'Total Assets', 'values'].values[0]
    total_liab = df.loc[df.fields == 'Total Liabilities', 'values'].values[0]
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]
    stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]
    eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]

    bvps = (total_assests-total_liab)/num_shares
    fair_value = (stock_price*num_shares)/(eps*bvps)
    return fair_value


# SGR
def get_sgr(df):
    drr = df.loc[df.fields == 'Desired Rate of Return', 'values'].values[0]/100
    dividend_yield = df.loc[df.fields == 'Dividend Yield', 'values'].values[0]
    eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]

    fair_value = drr*(1-(dividend_yield*eps))
    return fair_value

# PEG
def get_peg(df):
    pe_rate = df.loc[df.fields == 'P/E (T12M)', 'values'].values[0]
    eeg = df.loc[df.fields == 'Growth Rate', 'values'].values[0]/100

    fair_value = pe_rate/eeg
    return fair_value


# Earning Yield
def get_earning_yield(df):
    eps = df.loc[df.fields == 'EPS (T12M)', 'values'].values[0]
    stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]

    fair_value = eps/stock_price
    return fair_value

# ROCE 
def get_roce(df):
    op_revenue = df.loc[df.fields == 'Operating Revenue', 'values'].values[0]
    op_expenses = df.loc[df.fields == 'Operating Expenses', 'values'].values[0]
    total_equity = df.loc[df.fields == 'Total Equity', 'values'].values[0]
    total_debt = df.loc[df.fields == 'Total Debt', 'values'].values[0]

    fair_value = (op_revenue-op_expenses)/(total_equity+total_debt)
    return fair_value


# NCAV
def get_ncav(df):
    current_assests = df.loc[df.fields == 'Current Assets', 'values'].values[0]
    total_liab = df.loc[df.fields == 'Total Liabilities', 'values'].values[0]
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]

    fair_value = (current_assests - total_liab)/num_shares
    return fair_value


# DYGR
def get_dygr(df):
    dividend_yield = df.loc[df.fields == 'Dividend Yield', 'values'].values[0]
    trailing_dividend_yield = df.loc[df.fields == '5 year Trailiing Dividend Yield', 'values'].values[0]

    fair_value = (dividend_yield-trailing_dividend_yield)/trailing_dividend_yield
    return fair_value


# Balance sheet strength
def get_balance_stength(df):
    current_assests = df.loc[df.fields == 'Current Assets', 'values'].values[0]
    current_liabilities = df.loc[df.fields == 'Current Liabilities', 'values'].values[0]

    fair_value = current_assests-(1.5*current_liabilities)
    return fair_value


# FCF yield
def get_fcf(df):
    fcf = df.loc[df.fields == 'Free Cash Flow', 'values'].values[0]
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]
    stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]

    fair_value = fcf/(num_shares*stock_price)
    return fair_value

# EV
def get_ev(df):
    num_shares = df.loc[df.fields == 'Share Issued', 'values'].values[0]
    stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]
    total_debt = df.loc[df.fields == 'Total Debt', 'values'].values[0]
    current_assests = df.loc[df.fields == 'Current Assets', 'values'].values[0]
    ebitda = df.loc[df.fields == 'EBITDA', 'values'].values[0]

    fair_value = ((stock_price*num_shares)+total_debt-current_assests)/ebitda
    return fair_value