import streamlit as st
import pandas as pd
import numpy as np

st.title('List of companies based on filters')

ticker_df = pd.read_csv('valid_tickers_score.csv', sep = ';')
ticker_filtered = ticker_df.sort_values(by = 'score', ascending = False)

ticker_filtered = ticker_filtered[['ticker', 'score', 'eps', 'dcf10', 'balance_strength']]

score_range = ticker_filtered.score
score_silder = st.slider('SCORE filter', int(min(score_range)), int(max(score_range)), 20)
ticker_filtered = ticker_filtered[ticker_filtered.score >= score_silder]

balance_strength_range = ticker_filtered.balance_strength
balance_strength_range_silder = st.slider('BALANCE STRENGTH filter', int(balance_strength_range.quantile(q=0.1)), int(balance_strength_range.quantile(q=0.8)), 0)
ticker_filtered = ticker_filtered[ticker_filtered.balance_strength >= balance_strength_range_silder]

eps_range = ticker_filtered.eps
eps_silder = st.slider('EPS filter', int(eps_range.quantile(q=0.1)), int(eps_range.quantile(q=0.8)), 0)
ticker_filtered = ticker_filtered[ticker_filtered.eps >= eps_silder]


st.dataframe(
    ticker_filtered,
    column_config={
        "ticker": "TICKERS",
        "eps": "EPS (TTM)",
        "dcf10": "D. Cash Flow (10 years)",
        "balance_strength": "BALANCE STRENGTH",
        "score": st.column_config.NumberColumn(
            "SCORE",
            help="Our own score metric",
            format="%d ⭐",
        ),
        #"url": st.column_config.LinkColumn("App URL"),
        # "views_history": st.column_config.LineChartColumn(
        #     "Views (past 30 days)", y_min=0, y_max=5000
        # ),
    },
    hide_index=True,
)

