from pathlib import Path
from labeling import CNNLabeling, YoloLabeling
from candlestick import CNNChart, YoloChart
from utils import increment_path

class Dataset:
    def __init__(self, name, img, method, market, train, valid, test, sample) -> None:
        self.name = name
        self.img = img
        self.method = method
        self.market = market
        self.train = train
        self.valid = valid
        self.test = test
        self.samplt =sample

        self.root = Path(increment_path(Path.cwd() / 'Dataset'))
        self.root.mkdir()


class CNNDataset(Dataset):
    def __init__(self, name, img, method, market, train, valid, test, sample, period, **kwargs) -> None:
        super().__init__(name, img, method, market, train, valid, test, sample)
        
        self.path = self.root / 'CNN' / self.name
        self.labeling =CNNLabeling(market=market, period=period)

class YoloDataset(Dataset):
    def __init__(self) -> None:
        super().__init__()