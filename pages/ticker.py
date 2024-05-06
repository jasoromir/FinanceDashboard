import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import math

from millify import millify, prettify

from constants import dict_names
from processing import get_data
import metrics as m
from scores import scores

st.title('Financial Dashboard')
ticker_list = ['AAPL', 'GOOG', 'MSFT', 'CHEMM.CO']
ticker_df = pd.read_csv('valid_tickers_score.csv', sep = ';')

sort_mode = st.sidebar.selectbox('Sort Tickers', ['Alphabetically', 'Score'], index = 1)
                     
if sort_mode == 'Alphabetically':
    ticker_list = list(ticker_df.sort_values(by = 'ticker')['ticker'])
else:
    ticker_list = list(ticker_df.sort_values(by = 'score', ascending = False)['ticker'])

ticker_name = st.sidebar.selectbox('Select Company Ticker', ticker_list)

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
stock_price = m.get_stock_price(df)
eps = m.get_eps(df)
pe = m.get_pe(df)
dcf10 = m.get_dcf(df, 10)
dcf5 = m.get_dcf(df, 5)
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


# metrics = [dcf10, dcf5, graham_growth,graham_number, buffet_ratio,roe,munger_multiplier,sgr,peg,earning_yield,roce,ncav,dygr,balance_strength,free_cash_flow,ev]

# check_metrics_nan = 0
# for metric in metrics:
#     if math.isnan(metric):
#         check_metrics_nan += 1

metrics_missing = []
for idx, row in df.iterrows():
    if math.isnan( row['values']):
        metrics_missing.append(row['fields'])


if len(metrics_missing) <= 2:
    help_str = ''
    final_score = 0
    # globals()[metric]
    for metric, weight in scores.items():
        if metric.startswith('eps'):
            score = (eps>0)
        elif metric.startswith('pe'):
            score = (pe<20)
        elif metric.startswith('dcf10'):
            score = (dcf10>stock_price)
        elif metric.startswith('roce'):
            score = (roce*100>20)
        elif metric.startswith('roe'):
            score = (roe*100>12)
        elif metric.startswith('sgr'):
            score = (sgr*100>10)
        elif metric.startswith('free_cash_flow'):
            score = (free_cash_flow>0.05)
        elif metric.startswith('peg'):
            score = (peg>1)
        elif metric.startswith('earning_yield'):
            score = (earning_yield>1)
        elif metric.startswith('munger_multiplier'):
            score = (munger_multiplier>15)
        elif metric.startswith('buffet_ratio'):
            score = (buffet_ratio>1)
        elif metric.startswith('ncav'):
            score = (ncav>stock_price)
        elif metric.startswith('dygr'):
            score = (dygr>1)
        final_score += score*weight
        if score == 0:
            help_str = f'{help_str} \n {metric}: 0,'
        else:
            help_str = f'{help_str} \n {metric}: {weight},'

    final_score = int(final_score)
    delta = int((final_score-20))
    st.metric('SCORE', final_score, delta,
                    help = help_str)
   


st.write(f'## Metrics')
col1, col2, col3 = st.columns(3)


# if check_metrics_nan > 2:
if len(metrics_missing) > 2:
    st.warning(f'Metrics are missing: {metrics_missing}')
else:
    delta =  millify(eps-0, precision = 2)
    col1.metric('EPS', millify(eps, precision = 2), delta,)
    delta =  millify(pe-20, precision = 2)
    col2.metric('P/E Ratio', millify(pe, precision = 2), delta, delta_color = 'inverse')
    col3.metric('', '')
    col3.metric('', '')
    col3.metric('', '')



    delta =  millify(dcf10-stock_price, precision = 2)
    col1.metric('10 years DCF', millify(dcf10, precision = 2), delta,
                help = "Estimates a stock's intrinsic value based on future cash flows (present value).")
    delta =  millify(dcf5-stock_price, precision = 2)
    col2.metric('5 years DCF', millify(dcf5, precision = 2), delta,
                help = "Estimates a stock's intrinsic value based on future cash flows (present value).")
    col3.metric('', '')
    col3.metric('', '')
    col3.metric('', '')

    delta =  millify(graham_number-stock_price, precision = 2)
    col1.metric('GRAHMAR NUMBER', millify(graham_number, precision = 2), delta, delta_color = 'inverse')
    col2.metric('GRAHMAR GROWTH', millify(graham_growth, precision = 2), 0, delta_color = 'off')
    col3.metric('', '')
    col3.metric('', '')

    delta =  millify(buffet_ratio-1, precision = 2)
    col1.metric('BUFFET RATIO', millify(buffet_ratio, precision = 2), delta, 
                help = "Similar to P/B ratio, compares stock price to book value per share")
    try:
        delta =  millify(sgr*100-10, precision = 2)
        col2.metric('SGR', millify(sgr*100, precision = 2), delta)
    except:
        delta = 0
        col2.metric('SGR', np.nan, delta,  delta_color = 'off',
                    help = "Estimates the maximum growth rate achievable without new debt or equity.")

    delta =  millify(roe*100-12, precision = 2)
    col3.metric('ROE', millify(roe*100, precision = 2), delta,
                help = "Return on a company's shareholders' equity")

    delta =  millify(munger_multiplier-15, precision = 2)
    col1.metric('MUNGER MULTIPLE', millify(munger_multiplier, precision = 2), delta, 
                help = "Combines profitability (P/E) and underlying value (P/B)")
    delta =  millify(peg-1, precision = 2)
    col2.metric('PEG', millify(peg, precision = 2), delta, delta_color = 'inverse', 
                help = "Compares valuation (P/E) to expected growth rate")
    delta =  millify(earning_yield-1, precision = 2)
    col3.metric('EARNING YIELD', millify(earning_yield, precision = 2), delta, 
                help = "Earnings per dollar invested in the stock price (inverse of P/E ratio).")

    delta =  millify(roce*100-20, precision = 2)
    col1.metric('ROCE', millify(roce*100, precision = 2), delta,
                help = "Return on a company's invested capital (debt & equity)")
    delta =  millify(ncav-stock_price, precision = 2)
    col2.metric('NCAV', millify(ncav, precision = 2), delta, 
                help = "Represents company value based on net current assets (current assets minus current liabilities).")
    try:
        delta =  millify(dygr-1, precision = 2)
        col3.metric('DYGR', millify(dygr, precision = 2), delta)
    except:
        delta =  0
        col3.metric('DYGR', np.nan, delta,  delta_color = 'off', 
                    help = "Growth rate of a company's dividends over time.")

    delta =  millify(balance_strength-0, precision = 2)
    col1.metric('BALANCE SHEET STRENGTH', millify(balance_strength, precision = 2), delta)
    delta =  millify(free_cash_flow-0.05, precision = 2)
    col2.metric('FCF YIELD', millify(free_cash_flow, precision = 2), delta,
                help = "Cash flow available to the company after expenses and capital expenditures.")
    delta =  millify(ev-12, precision = 2)
    col3.metric('EV', millify(ev, precision = 2), delta, delta_color = 'inverse')