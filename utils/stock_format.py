from datetime import datetime
from utils import dataframe_empty_handler
import numpy as np
import pandas as pd
from typing import List


@dataframe_empty_handler
def convert_format(stock: pd.DataFrame, date_format: str):
    '''
    stock: stock historical data
    date_format: format of Date column
    '''
    column = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
    # Delete useless column
    delete_col = set(stock.columns) - set(column)
    for i in delete_col:
        del stock[i]

    # convert Date format to %Y-%m-%d
    stock.Date = stock.Date.map(lambda x: convert_date_format(x, date_format))

    # remove 0 and set Date as index
    stock.replace(0, np.NaN, inplace=True)
    stock.dropna(inplace=True)
    stock.set_index('Date', inplace=True)
    return stock


@dataframe_empty_handler
def convert_feature_format(stock: pd.DataFrame, volume: bool, SMA: List[str], EMA: List[str], MACD=List[int]):
    if not volume:
        del stock['Volume']
        
    for span in SMA:
        stock[f'{span}SMA'] = stock['Close'].rolling(span).mean()
    for span in EMA:
        stock[f'{span}EMA'] = stock['Close'].ewm(span=span).mean()

    if not 0 in MACD:
        ema_short = stock['Close'].ewm(span=MACD[0]).mean()
        ema_long = stock['Close'].ewm(span=MACD[1]).mean()
        stock['MACD'] = ema_short - ema_long
        stock['MACD_Signal'] = stock['MACD'].ewm(span=MACD[2]).mean()
    
    # remove 0 and set Date as index
    stock.replace(0, np.NaN, inplace=True)
    stock.dropna(inplace=True)
    return stock


def convert_date_format(date, date_format):
    date = str(date)
    date_time = datetime.strptime(date, date_format)
    date = date_time.strftime("%Y-%m-%d")
    return date