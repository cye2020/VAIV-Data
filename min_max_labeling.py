import pandas as pd


def get_span_labeling(data: pd.DataFrame, span, priority):
    labeling_list = []
    for i in range(0, len(data), span):
        section = data.iloc[i:i+span]
        section = section.astype(int)
        min_date = section['Close'].idxmin()  # Date when close price is minimum in the section
        max_date = section['Close'].idxmax()  # Date when close price is maximum in the section
        
        labeling = pd.DataFrame({
            'Label': [1, 0],  # buy: 1, sell: 0
            'Date': [min_date, max_date],
            'Priority': [priority, priority],
        })
        labeling_list.append(labeling)
    return labeling_list


def minmax_labeling(data, period, span_thres):
    span = period
    priority = 1
    dividend = 2
    
    labeling_list = []
    while span > span_thres:
        span_labeling = get_span_labeling(data, span, priority)
        labeling_list += span_labeling
        priority += 1
        span = period // dividend
        dividend *= 2
    labeling = pd.concat(labeling_list).drop_duplicates(subset=['Date']).set_index('Label')
    return labeling