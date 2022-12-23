from stock import StockMarket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--market', '-m', nargs='+', type=str, dest='market', default='ALL',
        help='You can input a list of under options\n' + \
             'ALL: Stock market includes KOSPI, KOSDAQ, and KONEX\n' + \
             'KOSPI: Stock market includes KOSPI only\n' + \
             'KOSDAQ: Stock market includes KOSDAQ only\n' + \
             'KONEX: Stock market includes KONEX only'
    )
    args = parser.parse_args()

    for market in args.market:
        StockMarket(market.upper()).update_datas()