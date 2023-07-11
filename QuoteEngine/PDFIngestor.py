from Exceptions import InvalidFileFormatException
from .model import QuoteModel
from .IngestorInterface import IngestorInterface
from typing import List
import subprocess
import tempfile
import os


class PDFIngestor(IngestorInterface):
    """Class to represent pdf ingestor."""

    extensions = ['pdf']

    @classmethod
    def parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from pdf file."""
        if not cls.can_ingest(path):
            raise InvalidFileFormatException("Invalid file format")

        quotes = []
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            subprocess.call(['pdftotext', '-layout', path, tmp.name])
            tmp.seek(0)
            for line in tmp.readlines():
                line = line.strip('\n\r').strip()
                if len(line) > 0 and " - " in line:
                    quote = QuoteModel(*line.strip().split(" - "))
                    quotes.append(quote)
        os.remove(tmp.name)

        return quotes
