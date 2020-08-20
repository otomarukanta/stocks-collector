import csv
import io

import requests

from model import StockPrice

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
            stock_price = StockPrice(
                yyyymmdd=int(row[0].replace("-", "")),
                open=int(row[1]),
                high=int(row[2]),
                low=int(row[3]),
                close=int(row[4]),
                volume=int(row[5]),
                adjusted_close=int(row[6])
            )

            yield stock_price