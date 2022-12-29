import argparse
from labeling import CNNLabeling, YoloLabeling, Labeling
from stock import StockMarket
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 


def make_labeling(market, number, labeling: Labeling, start='2006', end='a'):
    tickers = StockMarket(market.upper()).tickers
    num = number if number else len(tickers)
    for ticker in tickers[:num]:
        labeling.process_labeling(ticker, start, end)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
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
    
    parser.add_argument(
        '--method', type=str, required=True, help='the method of labeling'
    )
    parser.add_argument(
        '--period', type=int, default=argparse.SUPPRESS, help='the trading period of a chart'
    )
    parser.add_argument(
        '--forecast-interval', '-interval', dest='interval', type=int, default=argparse.SUPPRESS,
        help='predict n interval after the last input period'
    )
    parser.add_argument(
        '--name', '-n', type=str, dest='name', default=None, help='the name of chart folder'
    )
    
    args = parser.parse_args()
    kwargs = args.__dict__

    for market in args.market:
        kwargs['market'] = market
        if args.cnn:
            labeling = CNNLabeling(**kwargs)
        else:
            labeling = YoloLabeling(**kwargs)
        make_labeling(market, args.number, labeling, args.start, args.end)