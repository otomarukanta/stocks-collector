import csv
import io
from logging import getLogger, StreamHandler, Formatter, DEBUG, log

import requests

from model import StockPrice

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class BaseClient():
    pass

class StockPriceClient(BaseClient):
    def fetch(self, code, year):
        res = requests.post(
            "https://kabuoji3.com/stock/file.php",
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},
            data={"code": code, "year": year}
        )
        
        reader = csv.reader(io.StringIO(res.text))

        # header2行をskip
        next(reader)
        next(reader)

        for row in reader:
            try:
                stock_price = StockPrice(
                    yyyymmdd=int(row[0].replace("-", "")),
                    open=float(row[1]),
                    high=float(row[2]),
                    low=float(row[3]),
                    close=float(row[4]),
                    volume=int(row[5]),
                    adjusted_close=float(row[6])
                )
            except Exception as e:
                logger.warn(e)
                continue


            yield stock_price