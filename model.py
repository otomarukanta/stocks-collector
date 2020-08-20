from typing import NamedTuple

class StockPrice(NamedTuple):
    yyyymmdd: int
    open: int
    high: int
    low: int
    close: int
    volume: int
    adjusted_close: int