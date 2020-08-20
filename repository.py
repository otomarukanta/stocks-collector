from datetime import datetime
import io
from typing import Any, Dict, Iterable

from fastavro import writer
from fastavro.schema import parse_schema
from google.cloud import storage

from model import StockPrice
from util import generate_avro_schema

class BaseRepository():
    def __init__(self, client: storage.Client, bucket_name: str):
        self.bucket = client.get_bucket(bucket_name)

class StockPriceRepository(BaseRepository):
    def store(self, prices: Iterable[StockPrice], code: int, year: int):
        schema: Dict[str, Any] = parse_schema(generate_avro_schema(prices))
        fo = io.BytesIO()
        writer(fo, schema, [x._asdict() for x in prices])
        fo.seek(0)

        blob = self.bucket.blob(f'code={code}/year={year}/file.avro')
        blob.upload_from_file(fo)