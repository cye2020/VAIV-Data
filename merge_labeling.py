import pandas as pd
import numpy as np
import torch
from candlestick import YoloChart
from stock import Stock


def claculate_profit(left_close, right_close):
    return (right_close - left_close) / left_close * 100


def minmax_drange(stock: pd.DataFrame, last_date, left_thres, right_thres, temp) -> list:
    '''
    left profit: the percentage of profit between leftmost candlestick and minmax candlestick
    right profit: the percentage of profit between minmax candlestick and rightmost candlestick
    
    left_thres: float
        left profit threshold
    right_thres: float
        right profit threshold
    
    return: list
        the minimum date range that absolute value of profit is more than threshold
    '''
    close = stock.Close.loc[last_date]
    left_close = stock.Close.loc[:last_date].iloc[:-1].iloc[::-1]
    right_close = stock.Close.loc[last_date:].iloc[1:]
    left_most = last_date
    right_most = last_date

    for left, lclose in left_close.items():
        profit = temp*claculate_profit(lclose, close)
        if profit >= left_thres:
            left_most = left
            break
        if profit < 0:
            break

    for right, rclose in right_close.items():
        profit = -temp*claculate_profit(close, rclose)
        if profit >= right_thres:
            right_most = right
            break
        if profit < 0:
            break

    return stock.loc[left_most:right_most].index.tolist()


def merge_labeling(stock: pd.DataFrame, ticker, last_date, minmax: pd.DataFrame, patterns: pd.DataFrame, config, left_thres, right_thres):
    labeling_list = []
    before_drange = {'Label': -1, 'Date': 'empty', 'Range': []}
    chart = YoloChart(market=Stock(ticker).market, exist_ok=True, **config)
    pixel = chart.load_pixel_coordinates(ticker=ticker, last_date=last_date)
    dates = stock.index.tolist()

    for row in minmax.to_dict('records'):
        label = int(row.get('Label'))
        minmax_date = row.get('Date')
        prior = int(row.get('Priority'))
        
        temp = -1 if label==1 else 1
        
        drange = minmax_drange(stock, minmax_date, left_thres, right_thres, temp)
        condition1 = drange.index(minmax_date) in [0, len(drange) - 1]
        condition2 = dates.index(minmax_date) not in [0, len(dates) - 1]
        condition3 = len(drange) < 3
        if condition1 & condition2 | condition3:
            continue
        
        pattern = []
        
        for row in patterns[(patterns.index // 5) == (1 - label)].to_dict('records'):
            pattern_drange = row.get('Range').split('/')
            intersection = list(set(drange).intersection(pattern_drange))
            if len(intersection) > 0:
                drange = list(set(drange).union(pattern_drange))
                pattern.append(row.get('Pattern'))
        pattern = list(set(pattern))

        # remove local minimum
        if before_drange.get('Label') == label:
            close = temp*  stock.Close.loc[minmax_date]
            before_close = temp * stock.Close.loc[before_drange.get('Date')]
            if close < before_close:
                continue
            else:
                labeling_list.pop()

        xyxy = get_xyxy(pixel, drange)
        xywh = xyxy_to_xywh(chart.size, xyxy)

        df = pd.DataFrame({
            'Label': [label],
            'CenterX': [xywh[0]],
            'CenterY': [xywh[1]],
            'Width': [xywh[2]],
            'Height': [xywh[3]],
            'Range': ['/'.join(sorted(drange))],
            'Pattern': ['/'.join(pattern)],
            'Priority': [prior],
        })
        labeling_list.append(df)
        before_drange = {'Label': label, 'Date': minmax_date, 'Range': drange}
    try:
        labeling = pd.concat(labeling_list)
    except ValueError:  # minmax나 pattern이 없다
        print('MinMax or Pattern is empty!')
        print(ticker, last_date)
        return None

    return labeling


def get_xyxy(pixel, drange):
    '''
    Convert Date Range to bbox
    '''
    xmins = []
    ymins = []
    xmaxs = []
    ymaxs = []
    for date in drange:
        xmin, ymin, xmax, ymax = pixel.loc[date, 'Xmin':'Ymax'].tolist()
        xmins.append(xmin)
        ymins.append(ymin)
        xmaxs.append(xmax)
        ymaxs.append(ymax)
    return [min(xmins), min(ymins), max(xmaxs), max(ymaxs)]


def xyxy_to_xywh(size, xyxy):
    shape = (size[1], size[0], 3)
    gn = torch.tensor(shape)[[1, 0, 1, 0]]
    xywh = (
        xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn
    ).view(-1).tolist()  # normalized xywh
    return np.round(xywh, 6)


# from yolov7 utils.general
def xyxy2xywh(x):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = (x[:, 0] + x[:, 2]) / 2  # x center
    y[:, 1] = (x[:, 1] + x[:, 3]) / 2  # y center
    y[:, 2] = x[:, 2] - x[:, 0]  # width
    y[:, 3] = x[:, 3] - x[:, 1]  # height
    return y