import pandas as pd
from pathlib import Path
from stock import Stock
from utils import dataframe_empty_handler

class Labeling:
    def __init__(self, method) -> None:
        self.path = Path.cwd() / 'Labeling'
        self.method = method
        
    def load_labeling(self):
        pass
    

class CNNLabeling(Labeling):
    def __init__(self, period, interval) -> None:
        '''
        period: int
            trading period (= the number of candlestick chart candles)
            input n period stock data to model
        interval: int
            forecast interval
            predict n interval after the last input period
        '''
        super().__init__()
        self.path = self.path / 'CNN' / self.method
        self.period = period
        self.interval = interval
       
    def process_labeling(self, ticker, market='ALL'):
        stock = Stock(ticker, market)
        data = stock.load_data()
        dates = data.index.tolist()
        
        rows = [self.load_labeling()]
        for i in range(len(data)):
            c = data.iloc[i: i + self.period, :]  # trading(input) data
            try:
                f = data.iloc[i + self.period + self.interval - 1, :]  # forecast answer data
            except IndexError:
                continue
            
            starting = 0
            endvalue = 0
            label = ""
            
            if len(c) == self.period:
                if self.method[1:] == "%_01_2":
                    starting = c.iloc[-1, 'Close']
                    endvalue = f['Close']
                    
                    if endvalue >= (1 + (int(self.method[0])/100)) * starting:
                        label = 1
                    elif endvalue < starting:
                        label = 0
                    else:
                        continue

                else:
                    return
                
                row = pd.DataFrame({
                    'Date': [dates[i]],
                    'Ticker': [ticker],
                    'Label': [label]
                })
                rows.append(row)
            
        labeling = pd.concat(rows)
        labeling.to_csv(self.path / f'{self.period}days_{self.interval}after.csv', index=False)
    
    @dataframe_empty_handler
    def load_labeling(self):
        super().load_labeling()
        labeling = pd.read_csv(self.path / f'{self.period}days_{self.interval}after.csv', index_col=0)
        self.labeling = labeling
        return labeling


class YoloLabeling(Labeling):
    def __init__(self) -> None:
        super().__init__()