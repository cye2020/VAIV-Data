from pathlib import Path
from stock import Stock

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
        interval: int
            forecast interval
        '''
        super().__init__()
        self.path = self.path / 'CNN'
        self.period = period
        self.interval = interval
        
    def process_labeling(self, ticker, market='ALL'):
        stock = Stock(ticker, market)
        data = stock.load_data()
        
        
class YoloLabeling(Labeling):
    def __init__(self) -> None:
        super().__init__()