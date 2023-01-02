from tqdm import tqdm
import requests
import time
import pandas as pd
from pathlib import Path
import FinanceDataReader as fdr
from pykrx.website import krx
from pykrx import stock
import sys
p = Path.absolute(Path.cwd().parent)
sys.path.append(str(p))
from Data.utils import convert_format, convert_feature_format, dataframe_empty_handler
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)


krx_market = {'STK': 'KOSPI', 'KSQ': 'KOSDAQ', 'KNX': 'KONEX'}
class Stock:
    def __init__(self, ticker, market='ALL') -> None:
        '''
        p: path for historical data
        '''
        self.ticker = ticker
        self.market = krx_market.get(krx.get_stock_ticekr_market(ticker)) if market=='ALL' else market
        self.path = Path.cwd() / 'Stock' / self.market.capitalize()
        self.path.mkdir(parents=True, exist_ok=True)
        
    def download_data(self, start=None, end=None) -> pd.DataFrame:
        '''
        Download historical data from FinanceDatareader
        start: start date of historical data
        end: end date of historical data
        '''
        data = fdr.DataReader(self.ticker, start=start, end=end).reset_index(level=0)
        self.data = convert_format(data, '%Y-%m-%d %H:%M:%S')
        return self.data
    
    
    @dataframe_empty_handler
    def save_data(self) -> pd.DataFrame:
        '''
        Save historical data to the path
        '''
        self.data.to_csv(self.path / f'{self.ticker}.csv')
        return self.data
    
    @dataframe_empty_handler
    def load_data(self) -> pd.DataFrame:
        '''
        Load historical data from the path
        '''
        self.data = pd.read_csv(self.path / f'{self.ticker}.csv', index_col='Date', engine='python', error_bad_lines=False)
        return self.data
    
    @dataframe_empty_handler
    def update_data(self) -> pd.DataFrame:
        '''
        Update historical data
        '''
        self.download_data()
        self.save_data()
        return self.data


class FeatureStock(Stock):
    def __init__(self, ticker, market='ALL', volume=False, SMA=[], EMA=[], MACD=[0, 0, 0]) -> None:
        '''
        volume: if include volume feature, True. Else, False.
        SMA: simple moving average period list
        EMA: exponential moving average period list
        MACD: [short period, longer period, oscillator period]
        '''
        super().__init__(ticker, market)
        self.volume = volume
        self.SMA = SMA
        self.EMA = EMA
        self.MACD = MACD
        
    def download_data(self, start=None, end=None) -> pd.DataFrame:
        data = super().download_data(start, end)
        self.data = convert_feature_format(data, self.volume, self.SMA, self.EMA, self.MACD)
        return self.data
    
    def load_data(self) -> pd.DataFrame:
        data = super().load_data()
        self.data = convert_feature_format(data, self.volume, self.SMA, self.EMA, self.MACD)
        return self.data
    
    def save_data(self) -> pd.DataFrame:
        return super().save_data()
    
    def update_data(self) -> pd.DataFrame:
        return super().update_data()


class StockMarket:
    def __init__(self, market='ALL') -> None:
        self.market =  market.upper()
        self.tickers = sorted(stock.get_market_ticker_list(market=self.market))
        
    def update_datas(self):
        '''
        If you want to see progress bar, modify code to
            for i, ticker in enumerate(tqdm(self.tickers)):
        '''
        update_tickers(self.tickers, self.market)
        print(f'Make {self.market} Stocks Complete!')


def update_tickers(tickers, market='ALL'):
    error_tickers = list()
    for i, ticker in enumerate(tqdm(tickers)):
        s = Stock(ticker, market=market)
        try:
            s.update_data()
        except requests.exceptions.ChunkedEncodingError:
            time.sleep(1)
            error_tickers.append(ticker)
    if error_tickers:
        update_tickers(error_tickers, market)