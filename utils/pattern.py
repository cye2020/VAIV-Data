from typing import List

class CandleStick:
    def __init__(self, open=0, high=0, low=0, close=0) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        
        self.body = open - close
        self.upper_shadow = high - max(open, close)
        self.lower_shadow = min(open, close) - low
        self.candle = high - low
        
    def bullish(self):
        return self.open < self.close
    
    def bearish(self):
        return self.open > self.close


class Pattern:
    def __init__(self, num) -> None:
        '''
        num: int
            How many candlestick is needed for checking pattern
        '''
        self.num = num
        self.conditions = list()
    
    def __call__(self, date, section) -> bool:
        dates = section.index.tolist()
        i = dates.index(date)
        
        if i < (len(dates) - (self.num - 1)):
            candlesticks = [CandleStick(*tuple(section.loc[dates[i+n], 'Open':'Close'].tolist())) \
                for n in range(self.num)]
            return self.condition_check(candlesticks)
        return False
    
    def condition_check(self, candlesticks):
        check = []
        for condition in self.conditions:
            check.append(condition(candlesticks))
        return False not in check  # return True when satisfying all condition
            

class Bullish:
    def __init__(self) -> None:
        self.patterns = [self.BullishHarami(), self.BullishEngulfing(), \
            self.BullishDoji(), self.Hammer(), self.MoningStar()]
        
        self.nums = {p.__class__.__name__: p.num for p in self.patterns}

    def __call__(self, date, section) -> dict:
        result = dict()
        for pattern in self.patterns:
            result[pattern.__class__.__name__] = pattern(date, section)
        return result
    
    class BullishHarami(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bearish_candle, 0))
            self.conditions.append(Condition(bullish_candle, 1))
            self.conditions.append(Condition(close_under_open, 0, 1))
            self.conditions.append(Condition(close_under_open, 1, 0))
            self.conditions.append(Condition(big_body, 0, 0.6))

    class BullishEngulfing(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bearish_candle, 0))
            self.conditions.append(Condition(bullish_candle, 1))
            self.conditions.append(Condition(close_above_open, 0, 1))
            self.conditions.append(Condition(close_above_open, 1, 0))
            self.conditions.append(Condition(big_body, 1, 0.6))

    class BullishDoji(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bearish_candle, 0))
            self.conditions.append(Condition(lower, 1, 0))
            self.conditions.append(Condition(gravestone, 1, 3, 1, 1))
            self.conditions.append(Condition(big_body, 0, 0.6))

    class Hammer(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bearish_candle, 0))
            self.conditions.append(Condition(lower, 1, 0))
            self.conditions.append(Condition(dragonfly, 1, 0.3, 1, 2))
            self.conditions.append(Condition(big_body, 0, 0.6))


    class MoningStar(Pattern):
        def __init__(self, num=3) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bearish_candle, 0))
            self.conditions.append(Condition(bullish_candle, 2))
            self.conditions.append(Condition(big_body, 0, 0.6))
            self.conditions.append(Condition(close_above_open, 0, 1))
            self.conditions.append(Condition(close_under_open, 1, 2))
            self.conditions.append(Condition(small_body, 1, 0.3))
            self.conditions.append(Condition(bigger, 0, 1))
            self.conditions.append(Condition(bigger, 2, 1))
            self.conditions.append(Condition(lower, 1, 2))
            self.conditions.append(Condition(lower, 1, 0))
            self.conditions.append(Condition(high_under_open, 1, 0))
            self.conditions.append(Condition(high_under_close, 1, 2))


class Bearish:
    def __init__(self) -> None:
        self.patterns = [self.BearishHarami(), self.BearishEngulfing(), \
            self.GravestoneDoji(), self.HangingMan(), self.EveningStar()]

        self.nums = {p.__class__.__name__: p.num for p in self.patterns}

    def __call__(self, date, section) -> dict:
        result = dict()
        for pattern in self.patterns:
            result[pattern.__class__.__name__] = pattern(date, section)
        return result

    class BearishHarami(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bullish_candle, 0))
            self.conditions.append(Condition(bearish_candle, 1))
            self.conditions.append(Condition(close_above_open, 0, 1))
            self.conditions.append(Condition(close_above_open, 1, 0))
            self.conditions.append(Condition(big_body, 0, 0.6))

    class BearishEngulfing(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bullish_candle, 0))
            self.conditions.append(Condition(bearish_candle, 1))
            self.conditions.append(Condition(close_under_open, 0, 1))
            self.conditions.append(Condition(close_under_open, 1, 0))
            self.conditions.append(Condition(big_body, 1, 0.6))


    class GravestoneDoji(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bullish_candle, 0))
            self.conditions.append(Condition(higher, 1, 0))
            self.conditions.append(Condition(gravestone, 1, 3, 1, 1))
            self.conditions.append(Condition(big_body, 0, 0.6))


    class HangingMan(Pattern):
        def __init__(self, num=2) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bullish_candle, 0))
            self.conditions.append(Condition(higher, 1, 0))
            self.conditions.append(Condition(dragonfly, 1, 0.3, 1, 2))
            self.conditions.append(Condition(big_body, 0, 0.6))


    class EveningStar(Pattern):
        def __init__(self, num=3) -> None:
            super().__init__(num)
            self.conditions.append(Condition(bullish_candle, 0))
            self.conditions.append(Condition(bearish_candle, 2))
            self.conditions.append(Condition(big_body, 0, 0.6))
            self.conditions.append(Condition(close_under_open, 0, 1))
            self.conditions.append(Condition(close_above_open, 1, 2))
            self.conditions.append(Condition(small_body, 1, 0.3))
            self.conditions.append(Condition(bigger, 0, 1))
            self.conditions.append(Condition(bigger, 2, 1))
            self.conditions.append(Condition(higher, 1, 2))
            self.conditions.append(Condition(higher, 1, 0))
            self.conditions.append(Condition(high_under_open, 1, 0))
            self.conditions.append(Condition(high_under_close, 1, 2))


class Condition:
    def __init__(self, func, *args) -> None:
        self.func = func
        self.args = args
    
    def __call__(self, candlesticks: List[CandleStick]) -> bool:
        return self.func(candlesticks, *self.args)


def bullish_candle(candlesticks: List[CandleStick], n=0):
    '''
    n: int
        index of candlestick to check bullish
    '''
    c = candlesticks[n]
    return c.bullish()


def bearish_candle(candlesticks: List[CandleStick], n=0):
    '''
    n: int
        index of candlestick to check bearish
    '''
    c = candlesticks[n]
    return c.bearish()


def close_under_open(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to compare close with another candlestick's open
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.close < c2.open


def close_above_open(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to compare close with another candlestick's open
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.close > c2.open


def high_under_open(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to compare high with another candlestick's open
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.high < c2.open


def high_under_close(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to compare high with another candlestick's close
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.high < c2.close


def lower(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to check if its low is lower than another candlestick's low
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.low < c2.low


def higher(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to check if its high is higher than another candlestick's high
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.high > c2.high


def bigger(candlesticks: List[CandleStick], n1=0, n2=1):
    '''
    n1: int
        index of candlestick to check if its body is bigger than another candlestick's body
    n2: int
        index of another candlestick
    '''
    c1 = candlesticks[n1]
    c2 = candlesticks[n2]
    return c1.body > c2.body


def big_body(candlesticks: List[CandleStick], n=0, ratio=0.6):
    '''
    n: int
        index of candlestick to check the ratio of body
    ratio: float
        if body account for above 'ratio' of candle, it is big body
    '''
    c = candlesticks[n]
    return c.body > ratio * c.candle


def small_body(candlesticks: List[CandleStick], n=0, ratio=0.3):
    '''
    n: int
        index of candlestick to check the ratio of body
    ratio: float
        if body account for under 'ratio' of candle, it is big body
    '''
    c = candlesticks[n]
    return c.body < ratio * c.candle


def gravestone(candlesticks: List[CandleStick], n=0, ratio1=3, ratio2=1, ratio3=1):
    '''
    n: int
        index of candlestick to check gravestone doji
    ratio1, ratio2, ratio3: float
        upper_shadow: body: lower_shadow = ratio1: ratio2: ratio3
    '''
    c = candlesticks[n]
    check1 = c.upper_shadow * ratio2 > c.body * ratio1
    check2 = c.upper_shadow * ratio3 > c.lower_shadow * ratio1
    return check1 & check2


def dragonfly(candlesticks: List[CandleStick], n=0, ratio1=0.3, ratio2=1, ratio3=2):
    '''
    n: int
        index of candlestick to check dragonfly doji
    ratio1, ratio2, ratio3: float
        upper_shadow: body: lower_shadow = ratio1: ratio2: ratio3
    '''
    c = candlesticks[n]
    check1 = c.lower_shadow * ratio2 > c.body * ratio3
    check2 = c.upper_shadow * ratio2 > c.body * ratio1
    return check1 & check2