from typing import NamedTuple

class StockPrice(NamedTuple):
    yyyymmdd: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: float