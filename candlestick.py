import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
from stock import FeatureStock
from utils import candlestick_ochl, volume_overlay, dataframe_empty_handler, increment_path


class CandlstickChart:
    def __init__(self, market: str=None, size=None, period=None, linespace=None, candlewidth=None, linewidth=None, style=None, name=None, exist_ok=None, **kwargs) -> None:
        '''
        size: [width, height]
            the size of chart image
        period: int
            the trading period of a chart
        linespace: float
            the distance of each candle
        candlewidth: float
            the width of each candle
        linewidth: float
            the width of moving averages
        style: str
            plot style of matplotlib (ex. default: white background, dark_style: dark background)
        '''
        if 'undefined' in kwargs:
            return
        self.market = market.capitalize()
        self.size = size
        self.period = period
        self.linespace = linespace
        self.candlewidth = candlewidth
        self.linewidth = linewidth
        self.style = style
        self.set_default(**kwargs)
        self.path = Path(increment_path(Path.cwd() / 'Image' / (f'{size[0]}x{size[1]}' \
            if not name else name), exist_ok=exist_ok, sep='_'))
        name = self.path.name
        self.path = self.path / self.market
        (self.path / 'images').mkdir(parents=True, exist_ok=True)
        (self.path / 'pixels').mkdir(parents=True, exist_ok=True)
        try:
            info = pd.read_csv(Path.cwd() / 'Image' / 'info.csv', index_col='Name')
        except FileNotFoundError:
            info = pd.DataFrame()

        new_info = pd.DataFrame({
            'Name': [name],
            'Size': [f'{size[0]}x{size[1]}'],
            'period': [period],
            'linespace': [linespace],
            'candlewidth': [candlewidth],
            'linewidth': [linewidth],
            'style': [style],
            'Volume': [self.feature.get('volume')],
            'SMA': ['_'.join(self.feature.get('SMA'))],
            'EMA': ['_'.join(self.feature.get('EMA'))],
            'MACD': ['_'.join(map(str, self.feature.get('MACD')))],
            'UpColor': [self.color.get('up')],
            'DownColor': [self.color.get('down')],
            'SMAColor': ['_'.join(self.color.get('SMA'))],
            'EMAColor': ['_'.join(self.color.get('EMA'))],
            'MACDColor': ['_'.join(self.color.get('MACD'))],
        })
        info = pd.concat([info, new_info.set_index('Name')])
        info = info[~info.index.duplicated(keep='last')]
        info.to_csv(Path.cwd() / 'Image' / 'info.csv')
        
    def set_default(
        self,
        volume=False, SMA=[], EMA=[], MACD=[0, 0, 0],
        UpColor='#77d879', DownColor='#db3f3f', SMAColor=[], EMAColor=[], MACDColor=[],
        **kwargs
    ):
        '''
        feature: dict
            Determine whether or not to use Volume, SMA, EMA, or MACD
            {'volume': bool, 'SMA': [periods], 'EMA': [periods], 'MACD': [short, long, signal]}
        color: dict
            colors of each feature
            {'up': bullish candlesticks, 'down': bearish candlesticks, 'SMA': [each SMA], 'EMA': [each 
            EMA], 'MACD': [MACD, MACD oscillator]}
        '''
        self.feature = {'volume': volume, 'SMA': SMA, 'EMA': EMA, 'MACD': MACD}
        self.color = {'up': UpColor, 'down': DownColor, 'SMA': SMAColor, 'EMA': EMAColor, 'MACD': MACDColor}
        
    
    @dataframe_empty_handler
    def make_chart(self, ticker, last_date, pixel=True):
        '''
        ticker: str
        last_date: str
            the last candle (%Y-%m-%d)
        pixel: bool
            whether to save pixel coordinates. True when making yolo chart
        '''
        stock = FeatureStock(ticker, self.market, **self.feature)
        data = stock.load_data()
        dates = data.index.tolist()
        trade_index = dates.index(last_date)
        start_index = trade_index - self.period + 1
        
        if start_index < 0:
            return
        
        start = dates[start_index]
        c = data.loc[start:last_date]
        
        plt.style.use(self.style)
        num, ax = subplots(self.feature.get('volume'), self.feature.get('MACD'))
        fig = plt.figure(figsize=(self.size[0]/100, self.size[1]/100))
        ax1 = fig.add_subplot(ax[0])  # subplot of candlestick and moving averages
        
        # remove grid, labels, axis, padding
        ax1.grid(False)
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        ax1.axis('off')
        plt.tight_layout(pad=0)
        fig.set_constrained_layout_pads(w_pad=0, h_pad=0)
        
        t = np.arange(1, self.period * self.linespace+1, self.linespace)
        quote = c[['Open', 'Close', 'High', 'Low']]
        quote.insert(0, 't', t)
        quote.reset_index(drop=True, inplace=True)
        
        lines, patches = candlestick_ochl(
            ax1, quote.values, width=self.candlewidth,
            colorup=self.color.get('up'), colordown=self.color.get('down'), alpha=None
        )
        
        for i, span in enumerate(self.feature.get('SMA')):
            ax1.plot(
                c[f'{span}SMA'], linewidth=self.linewidth,
                color=self.color.get('SMA')[i], alpha=None
            )
            
        for i, span in enumerate(self.feature.get('EMA')):
            ax1.plot(
                c[f'{span}EMA'], linewidth=self.linewidth,
                color=self.color.get('EMA')[i], alpha=None
            )
            
        if self.feature.get('volume'):
            ax2 = fig.add_subplot(ax[1])
            bc = volume_overlay(
                ax2, c['Open'], c['Close'], c['Volume'], width=1,
                colorup=self.color.get('up'), colordown=self.color.get('down'), alpha=None,
            )
            ax2.add_collection(bc)
            ax2.grid(False)
            ax2.set_xticklabels([])
            ax2.set_yticklabels([])
            ax2.xaxis.set_visible(False)
            ax2.yaxis.set_visible(False)
            ax2.axis('off')
        
        if not 0 in self.feature.get('MACD'):
            ax3 = fig.add_subplot(ax[num])
            ax3.plot(c['MACD'], linewidth=1, color='red', alpha=None)
            ax3.plot(c['MACD_Signal'], linewidth=1, color='white', alpha=None)
            ax3.grid(False)
            ax3.set_xticklabels([])
            ax3.set_yticklabels([])
            ax3.xaxis.set_visible(False)
            ax3.yaxis.set_visible(False)
            ax3.axis('off')
        
        name = f'{ticker}_{last_date}'
        fig.savefig(self.path / 'images' / f'{name}.png')
        pil_image = Image.open(self.path / 'images' / f'{name}.png')
        rgb_image = pil_image.convert('RGB')
        rgb_image.save(self.path / 'images' / f'{name}.png')
        
        if pixel:
            pixel_coordinates = get_pixel(self.size, lines, patches, fig, c)
            pixel_coordinates.to_csv(self.path / 'pixels' / f'{name}.csv')

    def load_pixel_coordinates(self, ticker, last_date):
        name = f'{ticker}_{last_date}'
        pixel_coordinates = pd.read_csv(self.path / 'pixels' / f'{name}.csv', index_col='Date')
        return pixel_coordinates

    def load_chart_path(self, ticker, last_date):
        name = f'{ticker}_{last_date}'
        return self.path / 'images' / f'{name}.png'


class CNNChart(CandlstickChart):
    def __init__(
        self,
        market='Kospi',
        size=[224, 224],
        period=20,
        linespace=1,
        candlewidth=0.8,
        linewidth=1,
        style='dark_background',
        name=None,
        exist_ok=False,
        **kwargs,
    ) -> None:
        super().__init__(market, size, period, linespace, candlewidth, linewidth, style, name, exist_ok, **kwargs)
    

class YoloChart(CandlstickChart):
    def __init__(
        self,
        market='Kospi',
        size=[1800, 650],
        period=245,
        linespace=1,
        candlewidth=0.8,
        linewidth=1800/224,
        style='default',
        name=None,
        exist_ok=False,
        **kwargs
    ) -> None:
        super().__init__(market, size, period, linespace, candlewidth, linewidth, style, name, exist_ok, **kwargs)
        

def subplots(volume, MACD):
    '''
    determine how many subplots you use
    '''
    tf_MACD = 0 not in MACD  # if plot MACD and oscillator
    tf = [volume, tf_MACD]
    ax = []
    count = tf.count(True)
    if count == 0:
        ax = [111]
    elif count == 1:
        ax = [211, 212]
    else:
        ax = [211, 223, 224]
    return count, ax


def get_pixel(size, lines, patches, fig, stock):
    height = size[1]
    xmin, xmax, ymin, ymax = [[] for _ in range(4)]

    for i in range(len(stock)):
        bbox_x = patches[i].get_window_extent(fig.canvas.get_renderer())
        bbox_y = lines[i].get_window_extent(fig.canvas.get_renderer())
        xmin.append(bbox_x.x0)
        ymin.append(height-bbox_y.y1)
        xmax.append(bbox_x.x1)
        ymax.append(height-bbox_y.y0)

    dates = stock.index.tolist()

    df = pd.DataFrame({
        'Date': dates,
        'Xmin': xmin, 'Ymin': ymin,
        'Xmax': xmax, 'Ymax': ymax
    })
    df.set_index('Date', inplace=True)
    return df


@dataframe_empty_handler
def get_config(name):
    info = pd.read_csv(Path.cwd() / 'Image' / 'info.csv', index_col='Name')
    raw = info.loc[name]
    config = raw.replace(np.nan, '')
    size = list(map(int, config['Size'].split('x')))
    period = int(config['period'])
    linespace = float(config['linespace'])
    candlewidth = float(config['candlewidth'])
    linewidth = float(config['linewidth'])
    style = config['style']
    volume = bool(config['Volume'])
    SMA = list(map(int, list(filter(None, config['SMA'].split(',')))))
    EMA = list(map(int, list(filter(None, config['EMA'].split(',')))))
    MACD = list(map(int, list(filter(None, config['MACD'].split(',')))))
    UpColor = config['UpColor']
    DownColor = config['DownColor']
    SMAColor = list(filter(None, config['SMAColor'].split(',')))
    EMAColor = list(filter(None, config['EMAColor'].split(',')))
    MACDColor = list(filter(None, config['MACDColor'].split(',')))
    
    config_dict = {
        'size': size,
        'period': period,
        'linespace': linespace,
        'candlewidth': candlewidth,
        'linewidth': linewidth,
        'style': style,
        'volume': volume,
        'SMA': SMA,
        'EMA': EMA,
        'MACD': MACD,
        'UpColor': UpColor,
        'DownColor': DownColor,
        'SMAColor': SMAColor,
        'EMAColor': EMAColor,
        'MACDColor': MACDColor
    }
    return config_dict