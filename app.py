import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

from millify import millify, prettify

from constants import dict_names
from processing import get_data
import metrics as m


st.title('Financial Dashboard')
ticker_name = st.sidebar.selectbox('Select Company Ticker', ['AAPL', 'GOOG', 'MSFT', 'CHEMM.CO'])

ticker = yf.Ticker(ticker_name)

company_name = ticker.info['longName']
sector = ticker.info['sector']
industry = ticker.info['industry']
website = ticker.info['website']
business_sumary = ticker.info['longBusinessSummary']

st.write(f'## Financial values for {company_name} ({ticker_name})')
st.write(f'Sector: {sector}')
st.write(f'Industry: {industry} ')
st.write(f'website: {website} ')
with st.expander('Company business summary'):
    st.write(f'{business_sumary}')


# GET DATA

df = get_data(ticker)
# df_show = df.copy()
# for field in list(df_show.fields):
#     try:
#         df_show.loc[df_show.fields == field, 'values'] = millify(df_show.loc[df_show.fields == field, 'values'], precision = 3)
#     except:
#         pass

with st.expander('Open to see detailed information'):
    st.table(df)

# GET METRICS
dfc10 = m.get_dfc(df, 10)
dfc5 = m.get_dfc(df, 5)
graham_growth = m.get_graham_growth(df)
graham_number = m.get_graham_number(df) 
buffet_ratio = m.get_buffet_ratio(df)
roe = m.get_roe(df)
munger_multiplier = m.get_munger_multiplier(df)
sgr = m.get_sgr(df)
peg = m.get_peg(df)
earning_yield = m.get_earning_yield(df)
roce =m.get_roce(df)
ncav = m.get_ncav(df)
dygr = m.get_dygr(df)
balance_strength = m.get_balance_stength(df)
free_cash_flow = m.get_fcf(df)
ev = m.get_ev(df)



st.write(f'## Metrics')
col1, col2, col3 = st.columns(3)


stock_price = df.loc[df.fields == 'Stock Price', 'values'].values[0]

delta =  millify(dfc10-stock_price, precision = 2)
col1.metric('10 years DCF', millify(dfc10, precision = 2), delta)
delta =  millify(dfc5-stock_price, precision = 2)
col2.metric('5 years DCF', millify(dfc5, precision = 2), delta)
col3.metric('', '')
col3.metric('', '')
col3.metric('', '')

delta =  millify(graham_number-stock_price, precision = 2)
col1.metric('GRAHMAR NUMBER', millify(graham_number, precision = 2), delta, delta_color = 'inverse')
col2.metric('GRAHMAR GROWTH', millify(graham_growth, precision = 2), 0, delta_color = 'off')
col3.metric('', '')
col3.metric('', '')

delta =  millify(buffet_ratio-1, precision = 2)
col1.metric('BUFFET RATIO', millify(buffet_ratio, precision = 2), delta)
delta =  millify(sgr*100-10, precision = 2)
col2.metric('SGR', millify(sgr*100, precision = 2), delta)
delta =  millify(roe*100-12, precision = 2)
col3.metric('ROE', millify(roe*100, precision = 2), delta)

delta =  millify(munger_multiplier-15, precision = 2)
col1.metric('MUNGER MULTIPLE', millify(munger_multiplier, precision = 2), delta)
delta =  millify(peg-1, precision = 2)
col2.metric('PEG', millify(peg, precision = 2), delta, delta_color = 'inverse')
delta =  millify(earning_yield-1, precision = 2)
col3.metric('EARNING YIELD', millify(earning_yield, precision = 2), delta)

delta =  millify(roce*100-20, precision = 2)
col1.metric('ROCE', millify(roce*100, precision = 2), delta)
delta =  millify(ncav-stock_price, precision = 2)
col2.metric('NCAV', millify(ncav, precision = 2), delta)
delta =  millify(dygr-1, precision = 2)
col3.metric('DYGR', millify(dygr, precision = 2), delta)

delta =  millify(balance_strength-0, precision = 2)
col1.metric('BALANCE SHEET STRENGTH', millify(balance_strength, precision = 2), delta)
delta =  millify(free_cash_flow-5, precision = 2)
col2.metric('FCF YIELD', millify(free_cash_flow, precision = 2), delta)
delta =  millify(ev-12, precision = 2)
col3.metric('EV', millify(ev, precision = 2), delta, delta_color = 'inverse')