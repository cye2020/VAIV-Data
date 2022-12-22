import pandas as pd

def dataframe_empty_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, KeyError, TypeError):
            return pd.DataFrame()
    return wrapper