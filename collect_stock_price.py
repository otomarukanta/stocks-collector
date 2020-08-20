from datetime import date
import os
import time
from typing import Any, Dict

import pandas as pd
from google.cloud import storage


from client import StockPriceClient
from repository import StockPriceRepository


def get_codes():
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    df = pd.read_excel(url)
    return df['コード'].values


client = StockPriceClient()
repo = StockPriceRepository(storage.Client(), os.environ['OUTPUT_BUCKET_NAME'])

year = date.today().year
for code in get_codes():
    prices = client.fetch(code, year)
    repo.store(prices, code, year)
    time.sleep(1)