# Data

Before training CNN and Yolov7 models, you must make dataset.

## 1. Installation
Install packages with:
```
pip install -r requirements.txt
```

## 2. Module
### 2.1 Download Stock OHLCV historical data
download stock historical data using [FinanceDataReader](https://github.com/financedata-org/FinanceDataReader)

```
# download all stock historical data in kospi and kosdaq
python make_stocks.py -m kospi kosdaq
```

Download Directory

```
Data
├── Stock
│   ├── Kosdaq
│       ├── 000250.csv
│       └── …
│   └── Kospi
│       ├── 000020.csv
│       └── …
```

### 2.2 Make Candlestick Chart
### 2.3 Update
### 2.4 Labeling
### 2.5 Make Dataset

```python
import 
```