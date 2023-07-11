from Exceptions import InvalidFileFormatException
from typing import List
from .IngestorInterface import IngestorInterface
from .model import QuoteModel
import pandas


class CSVIngestor(IngestorInterface):
    """Class to represent csv ingestor."""

    extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from csv file."""
        if not cls.can_ingest(path):
            raise InvalidFileFormatException("Invalid file format")

        df = pandas.read_csv(path, header=0)
        quotes = [QuoteModel(row['body'], row['author'])
                  for _, row in df.iterrows()]

        return quotes
