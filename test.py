import streamlit as st
import yfinance as yf
import pandas as pd
from PortfolioOptimizer import MarkowitzPortfolioOptimizer as mpo
from StockDataLoader import StockDataLoader as sdl
from stockList import StockSectors as sc
import json 

st.title("Markowitz Portfolio  Optimization")

sector_list = sc.get_sector_list()
dropdown_sectors = st.multiselect('Select Sector ',sector_list)
tickers=list()
# tickers=sc.get_sector_stocks(dropdown_sectors[0])
# print(dropdown_sectors)
if dropdown_sectors:
    for item in dropdown_sectors:
        if item == 'Auto':
            auto_list = sc.get_sector_stocks(item)
            tickers =auto_list
            
        elif item == 'Banking':
            banking_list = sc.get_sector_stocks(item)
            tickers =banking_list
            
        elif item == 'Finance':
            finance_list = sc.get_sector_stocks(item)
            tickers =finance_list
            
        elif item == 'IT':
            it_list = sc.get_sector_stocks(item)
            tickers =it_list
            
        elif item == 'FMCG':
            fmcg_list = sc.get_sector_stocks(item)
            tickers =fmcg_list

dropdown = st.multiselect('Select Tickers',tickers)
obj=sdl(dropdown)
df=obj.get_stock_data()
# start=st.date_input('Start',value=pd.to_datetime('2020-01-01'))
# end=st.date_input('Start',value=pd.to_datetime('today'))

option = st.select_slider(
     'Select your preferred portfolio return ',

  
     options=[str(i)+"%" for i in range(100)])
st.write('Chosen Return  Value is :', option)
return_expected = float(option[:-1])/100

if len(dropdown)>0:

    capital=st.number_input('Choose your Investment Amount in Rs. ')

    markowitzer= mpo(df)

    fit_data = markowitzer.fit()

    model_data= json.loads(fit_data)

    user_portfolio = markowitzer.get_portfolio(return_expected,capital)

    mvp_portfolio = markowitzer.get_least_volatility_portfolio(capital)

    SrMax_portfolio = markowitzer.get_SRmax_portfolio(capital)

    st.write('User Portfolio :',user_portfolio)
    st.write('Least Volatility Portfolio :',mvp_portfolio)
    st.write('SR Max Portfolio :',SrMax_portfolio)



# if len(dropdown)>0:
#     st.dataframe(df)
    
