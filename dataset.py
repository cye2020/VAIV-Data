'''
Dataset for CNN and Yolo
    Both train and valid are in one folder.
    However, test is divided by year.
    
    Finally, train, valid, and test folders are divided by label.


[Directory Example]

Dataset
├── CNN
│   ├── {name}
│   │   ├── train
│   │   │   ├── 0
│   │   │   └── 1
│   │   ├── valid
│   │   ├── test2019
│   │   └── test2020
'''
from pathlib import Path
import pandas as pd
import random
import shutil
from labeling import CNNLabeling, YoloLabeling
from candlestick import CandlstickChart, CNNChart, YoloChart, get_config
from utils import increment_path
import warnings
warnings.filterwarnings("ignore") 


class Dataset:
    def __init__(self, name, img, method, market, train, valid, test, sample, offset) -> None:
        self.name = name
        self.img = img
        self.method = method
        self.market = market
        self.train = train
        self.valid = valid
        self.test = test
        self.sample =sample
        self.offset = offset
        
        self.root = Path.cwd() / 'Dataset'
        self.root.mkdir(parents=True, exist_ok=True)
        self.chart = CandlstickChart(undefined=None)

    def make_dataset(self):
        pass
    
    def move_image(self, ticker, last_date, label, save_dir):
        img_from = self.chart.load_chart_path(ticker, last_date)
        img_to = save_dir / str(label) / img_from.name
        (save_dir / str(label)).mkdir(parents=True, exist_ok=True)
        try:
            shutil.copyfile(img_from, img_to)
        except FileNotFoundError:
            return


class CNNDataset(Dataset):
    def __init__(
        self,
        name: str =None,
        img: str ='224x224',
        method: str ='4%_01_2',
        market: str ='Kospi',
        train: list =[2006, 2018],
        valid: list =[2018, 2019],
        test: list = [2019, 2022],
        sample: list = [-1, -1, -1],
        interval: int = 5,
        offset: int = 1,
        exist_ok: bool = False,
        **kwargs
    ) -> None:
        super().__init__(name, img, method, market, train, valid, test, sample, offset)

        self.path = Path(increment_path(self.root / 'CNN' / self.name, exist_ok = exist_ok))

        config = get_config(name)
        self.chart = CNNChart(market=market, exist_ok=True, **config)
        self.labeling = CNNLabeling(market=market, period=self.chart.period, interval=interval, method=method)
        
    def make_dataset(self):
        super().make_dataset()
        l = self.labeling.load_labeling()  # labeling csv file
        
        train = l[(l['Date'] >= str(self.train[0])) & (l['Date'] < str(self.train[1]))]
        valid = l[(l['Date'] >= str(self.valid[0])) & (l['Date'] < str(self.valid[1]))]
        
        test_year = list(range(self.test[0], self.test[1]))
        test = dict()
        
        train = self.sampling(train, 0)
        valid = self.sampling(valid, 1)
        for year in test_year:
            test[year] = l[(l['Date'] >= str(year)) & (l['Date'] < str(year+1))]
            test[year] = self.sampling(test[year], 2)
        
        self.move_image(train, self.path / 'train')
        self.move_image(valid, self.path / 'valid')
        for year in test_year:
            self.move_image(test[year], self.path / f'test{year}')
        
    def sampling(self, labeling: pd.DataFrame, n):
        '''
        n: int
            0: train, 1: valid, 2: test
        '''
        labels = labeling['Label'].unique()
        index = labeling.index.tolist()
        offset_index = list(range(index[0], index[-1] + 1, self.offset))
        offset_labeling = labeling[labeling.index.isin(offset_index)]
        count = offset_labeling['Label'].value_counts().tolist()
        
        if self.sample[n] == -1:  # do not sample
            return offset_labeling

        if len(count) == len(labels):
            sample_index = list()
            num = min(*count, self.sample[n])
            for label in labels:
                label_index = offset_labeling[offset_labeling['Label'] == label].index.tolist()
                label_index = random.sample(label_index, num)
                sample_index += label_index
            sample_labeling = offset_labeling[offset_labeling.index.isin(sorted(sample_index))]
            return sample_labeling.reset_index(drop=True)
        else:
            raise Exception('There is not every label in this file')
    
    def move_image(self, labeling: pd.DataFrame, save_dir):
        '''
        move image from Image folder to Dataset folder
        '''
        for row in labeling.to_dict('records'):
            ticker = row['Ticker']
            last_date = row['Date']
            label = row['Label']
            
            super().move_image(ticker, last_date, label, save_dir)


class YoloDataset(Dataset):
    def __init__(
        self,
        name: str =None,
        img: str ='1800x650',
        method: str ='4%_01_2',
        market: str ='Kospi',
        train: list =[2006, 2018],
        valid: list =[2018, 2019],
        test: list = [2019, 2022],
        sample: list = [-1, -1, -1],
        offset: int = 1,
        exist_ok: bool = False,
        **kwargs
    ) -> None:
        super().__init__(name, img, method, market, train, valid, test, sample, offset)
        self.path = Path(increment_path(self.root / 'Tolo' / self.name, exist_ok = exist_ok))

        config = get_config(name)
        self.chart = YoloChart(market=market, exist_ok=True, **config)
        self.labeling = YoloLabeling(market=market, period=self.chart.period, method=method)
        
    def make_dataset(self):
        super().make_dataset()
        
    def move_image(self):
        super().move_image()
        