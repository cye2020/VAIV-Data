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
        self.conditions = []
    
    def __call__(self, date, section) -> bool:
        dates = section.index.tolist()
        i = dates.index(date)
        
        if i < (len(dates) - (self.num - 1)):
            candlesticks = [CandleStick(section.loc[dates[i+n], 'Open':'Close'].tolist()) \
                for n in range(self.num)]
            return self.condition_check(candlesticks)
        return False
    
    def condition_check(self, candlesticks):
        check = []
        for condition in self.conditions:
            check.append(condition(candlesticks))
        return False not in condition  # return True when satisfying all condition
            


class Bullish:
    def __init__(self) -> None:
        self.patterns = [self.BullishHarami, self.BullishEngulfing, self.BullishDoji, self.Hammer, self.MoningStar]

    def __call__(self, date, section) -> dict:
        result = dict()
        for pattern in self.patterns:
            result[pattern.__class__.__name__] = pattern(date, section)
        return result
    
    class BullishHarami(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)
            
    class BullishEngulfing(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)
    
    class BullishDoji(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)

    class Hammer(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)

    class MoningStar(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)


class Bearish:
    def __init__(self) -> None:
        self.patterns = [self.BearishHarami, self.BearishEngulfing, self.GravestoneDoji, self.HangingMan, self.EveningStar]
    
    class BearishHarami(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)

    class BearishEngulfing(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)
        
    class GravestoneDoji(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)

    class HangingMan(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)

    class EveningStar(Pattern):
        def __init__(self, num) -> None:
            super().__init__(num)
