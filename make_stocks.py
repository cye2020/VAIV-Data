from pathlib import Path
import argparse
import sys
p = Path.absolute(Path.cwd().parent)
sys.path.append(str(p))
from Data.stock import StockMarket

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--market', '-m', nargs='+', type=str, dest='market', default=['Kospi', 'kosdaq'],
        help='You can input a list of under options\n' + \
             'KOSPI: Stock market includes KOSPI only\n' + \
             'KOSDAQ: Stock market includes KOSDAQ only\n' + \
             'KONEX: Stock market includes KONEX only'
    )
    args = parser.parse_args()

    for market in args.market:
        StockMarket(market.upper()).update_datas()