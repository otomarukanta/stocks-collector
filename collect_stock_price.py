from datetime import date
import os
import time
from typing import Any, Dict
from logging import getLogger, StreamHandler, Formatter, DEBUG

import pandas as pd
from google.cloud import storage

from client import StockPriceClient
from repository import StockPriceRepository

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def get_codes():
    return [1413]
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    df = pd.read_excel(url)
    return df['コード'].values


client = StockPriceClient()
repo = StockPriceRepository(storage.Client(), os.environ['OUTPUT_BUCKET_NAME'])

year = date.today().year
for code in get_codes():
    logger.info(f"fetching code={code}, year={year}")
    prices = client.fetch(code, year)
    try:
        repo.store(prices, code, year)
    except StopIteration as e:
        logger.warn(f"code={code}, year={year} not found. %s")
        continue

    time.sleep(1)