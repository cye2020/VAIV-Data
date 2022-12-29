import argparse
from dataset import CNNDataset, YoloDataset


def make_dataset(**kwargs):
    kwargs['market'] = kwargs['market'][0]
    dataset = CNNDataset(**kwargs)
    dataset.make_dataset()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    base = parser.add_mutually_exclusive_group(required=True)
    base.add_argument(
        '--yolo', action='store_true', help='use default yolo chart setting'
    )
    base.add_argument(
        '--cnn', action='store_true', help='use default cnn chart setting'
    )

    parser.add_argument(
        '--name', '-n', type=str, dest='name', default=None, help='the name of dataset folder'
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
        '--train', nargs='+', type=int, default=[2006, 2018], help='train period'
    )
    parser.add_argument(
        '--valid', nargs='+', type=int, default=[2018, 2019], help='validation period'
    )
    parser.add_argument(
        '--test', nargs='+', type=int, default=[2019, 2022], help='test period'
    )
    parser.add_argument(
        '--sample', nargs='+', type=int, default=argparse.SUPPRESS,
        help='the number of each train, validation, test sample per label\n' + \
            '[train, valid, test/year]\n' + \
            '-1: do not sample. put all image in dataset (ex. [25000, 3000, -1])'
    )
    parser.add_argument(
        '--labeling', '-l', dest='method', type=str, required=True, help='Labeling folder (method)'
    )
    parser.add_argument(
        '--img', '-i', type=str, required=True, help='candlestick chart image folder'
    )
    parser.add_argument(
        '--offset', '-o', type=int, default=1, help='chart image shift by offset'
    )

    cnn = parser.add_argument_group('CNN', 'used in cnn only')
    cnn.add_argument(
        '--forecast-interval', '-interval', dest='interval', type=int, default=argparse.SUPPRESS,
        help='predict n interval after the last input period'
    )
    
    yolo = parser.add_argument_group('Yolo', 'used in yolo only')
    yolo.add_argument(
        '--prior-thres', '-prior', dest='prior', type=int, default=argparse.SUPPRESS,
        help='priority over prior-thres Date Range in Labeling is necessarily included in Dataset'
    )
    yolo.add_argument(
        '--pattern-thres', '-pattern', dest='pattern', type=int, default=argparse.SUPPRESS,
        help='priority over pattern-thres Date Range in Labeling is included in Dataset if there is pattern'
    )
    
    args = parser.parse_args()
    kwargs = args.__dict__
    print(args)
    make_dataset(**kwargs)