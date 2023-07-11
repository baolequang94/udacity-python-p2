from Exceptions import InvalidFileFormatException
from .model import QuoteModel
from .IngestorInterface import IngestorInterface
from typing import List


class TextIngestor(IngestorInterface):
    """Class to represent text ingestor."""

    extensions = ['txt']

    @classmethod
    def parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from txt file."""
        if not cls.can_ingest(path):
            raise InvalidFileFormatException("Invalid file format")

        quotes = []
        with open(path, "r") as f:
            for line in f:
                if " - " in line:
                    quote = QuoteModel(*line.strip().split(" - "))
                    quotes.append(quote)
        return quotes
