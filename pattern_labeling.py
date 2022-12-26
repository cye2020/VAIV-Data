import pandas as pd
from utils import Bullish, Bearish

def pattern_labeling(data: pd.DataFrame):
    bullish = Bullish()
    bearish = Bearish()
    
    dates = data.index.tolist()
    labeling_list = []
    for i, date in enumerate(dates):
        bullish_pattern = bullish(date, data)
        bearish_pattern = bearish(date, data)
        
        for pattern, check in bullish_pattern.items():
            label = list(bullish.nums.keys()).index(pattern)
            if check:
                bullish_labeling = pd.DataFrame({
                    'Label': [label],
                    'Range': '/'.join(dates[i:i+bullish.nums[pattern]]),
                    'Pattern': pattern
                })
                labeling_list.append(bullish_labeling)
                
        for pattern, check in bearish_pattern.items():
            label = list(bearish.nums.keys()).index(pattern)
            if check:
                bearish_labeling = pd.DataFrame({
                    'Label': [label],
                    'Range': '/'.join(dates[i:i+bearish.nums[pattern]]),
                    'Pattern': pattern
                })
                labeling_list.append(bearish_labeling)
    
    labeling = pd.concat(labeling_list).set_index('Label')
    return labeling