import argparse
from stock import StockMarket, Stock
from candlestick import CNNChart, YoloChart, CandlstickChart
import multiprocessing as mp
import warnings
warnings.filterwarnings(action='ignore')

def make_ticker_candlesticks(chart: CandlstickChart, ticker, market, start='2006', end='a'):
    data = Stock(ticker, market).load_data()
    dates = data.index.tolist()
    dates = [d for d in dates if (d >= start) & (d < end)]
    for last_date in dates:
        chart.make_chart(ticker, last_date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--name', '-n', type=str, dest='name', default=None, help='the name of chart folder'
    )
    parser.add_argument(
        '--exist-ok', action='store_true',
        help='existing project/name ok, do not increment'
    )
    parser.add_argument(
        '--market', '-m', nargs='+', type=str, dest='market', required=True,
        help='You can input a market under options\n' + \
             'KOSPI: Stock market includes KOSPI only\n' + \
             'KOSDAQ: Stock market includes KOSDAQ only\n' + \
             'KONEX: Stock market includes KONEX only'
    )
    parser.add_argument(
        '--number', '-num', type=int, dest='number', default=None,
        help='How many stock you make',
    )
    parser.add_argument(
        '--start', '-s', type=str, default='2006', help='Make chart that trade date >= start'
    )
    parser.add_argument(
        '--end', '-e', type=str, default='a', help='Make chart that trade date < end'
    )
    
    base = parser.add_mutually_exclusive_group(required=True)
    base.add_argument(
        '--yolo', action='store_true', help='use default yolo chart setting'
    )
    base.add_argument(
        '--cnn', action='store_true', help='use default cnn chart setting'
    )
    
    config = parser.add_argument_group('Chart Configure')
    config.add_argument(
        '--size', nargs='+', type=int, dest='size', default=argparse.SUPPRESS, help='the size of chart image'
    )
    config.add_argument(
        '--period', type=int, default=argparse.SUPPRESS, help='the trading period of a chart'
    )
    config.add_argument(
        '--linespace', '-ls', type=float, default=argparse.SUPPRESS, help='the distance of each candle'
    )
    config.add_argument(
        '--candlewidth', '-cw', type=float, default=argparse.SUPPRESS, help='the width of each candle'
    )
    config.add_argument(
        '--linewidth', '-lw', type=float, default=argparse.SUPPRESS, help='the width of moving averages'
    )
    config.add_argument(
        '--style', type=str, default=argparse.SUPPRESS,
        help='plot style of matplotlib (ex. default: white background, dark_style: dark background)'
    )
    
    feature = parser.add_argument_group('Feature')
    feature.add_argument(
        '--volume', '-v', type=bool, default=argparse.SUPPRESS, help='chart with volume'
    )
    feature.add_argument(
        '--SMA', '-sma', nargs='+', type=int, default=argparse.SUPPRESS, help='the list of Simple Moving Average period list'
    )
    feature.add_argument(
        '--EMA', '-ema', nargs='+', type=int, default=argparse.SUPPRESS, help='the list of Exponential Moving Average period list'
    )
    feature.add_argument(
        '--MACD', '-macd', nargs='+', type=int, default=argparse.SUPPRESS, help='MACD short period, long period, signal period'
    )
    
    color = parser.add_argument_group('Color')
    color.add_argument(
        '--UpColor', '-uc', type=str, default=argparse.SUPPRESS, help='the color of bullish candlesticks'
    )
    color.add_argument(
        '--DownColor', '-dc', type=str, default=argparse.SUPPRESS, help='the color of bearish candlesticks'
    )
    color.add_argument(
        '--SMAColor', '-sc', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of each SMA'
    )
    color.add_argument(
        '--EMAColor', '-ec', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of each EMA'
    )
    color.add_argument(
        '--MACDColor', '-mc', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of MACD and MACD oscillator'
    )
    args = parser.parse_args()
    
    kwargs = args.__dict__
    
    for market in args.market:
        tickers = StockMarket(market.upper()).tickers
        num = args.number if args.number else len(tickers)
        kwargs['market'] = market
        if args.cnn:
            chart = CNNChart(**kwargs)
        
        else:
            chart = YoloChart(**kwargs)
        
        with mp.Pool(10) as pool:
            args_list = [(chart, ticker, market, args.start, args.end) for ticker in tickers[:num]]
            result = pool.starmap_async(make_ticker_candlesticks, args_list)
            result.wait()