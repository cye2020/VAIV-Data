import pandas as pd

def merge_labeling(data, left_thres, right_thres):
    labeling_list = []
    before_drange = {'Label': -1, 'Date': 'empty', 'Range': []}
    