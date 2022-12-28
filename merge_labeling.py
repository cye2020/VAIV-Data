import pandas as pd


def minmax_drange(data, trade_date, left_thres, right_thres, label):
    pass

def merge_labeling(data, minmax: pd.DataFrame, patterns: pd.DataFrame, left_thres, right_thres):
    labeling_list = []
    before_drange = {'Label': -1, 'Date': 'empty', 'Range': []}
    
    for row in minmax.to_dict('records'):
        label = row.get('Label')
        trade_date = row.get('Date')
        prior = row.get('Priority')
        
        