import argparse
from pathlib import Path
import sys
p = Path.absolute(Path.cwd().parent)
sys.path.append(str(p))
from Data.stock import StockMarket
from Data.candlestick import CandlstickChart, get_config
import exchange_calendars as ecals
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def update_name_candlesticks(tickers, market, name, today):
    config = get_config(name)
    chart = CandlstickChart(**config, market=market, name=name, exist_ok=True)
    for ticker in tickers:
        chart.make_chart(ticker, today)


def DateCheck(today):
    XKRX = ecals.get_calendar('XKRX')
    return XKRX.is_session(today)


def update(market, name):
    today = datetime.now()
    today = today.strftime('%Y-%m-%d')
    if DateCheck(today):
        stockmarket = StockMarket(market.upper())
        stockmarket.update_datas()  # update stock
        tickers = stockmarket.tickers
        update_name_candlesticks(tickers, market, name, today)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name', '-n', type=str, dest='name', required=True, help='the name of chart folder'
    )
    parser.add_argument(
        '--market', '-m', nargs='+', type=str, dest='market', required=True,
        help='You can input a list of under options\n' + \
             'KOSPI: Stock market includes KOSPI only\n' + \
             'KOSDAQ: Stock market includes KOSDAQ only\n' + \
             'KONEX: Stock market includes KONEX only'
    )
    args = parser.parse_args()

    for market in args.market:
        update(market, args.name)