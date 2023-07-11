from Exceptions import InvalidFileFormatException
from .model import QuoteModel
from .IngestorInterface import IngestorInterface
from typing import List
import docx


class DocxIngestor(IngestorInterface):
    """Class to represent docx ingestor."""

    extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from docx file."""
        if not cls.can_ingest(path):
            raise InvalidFileFormatException("Invalid file format")

        quotes = []
        doc = docx.Document(path)
        for para in doc.paragraphs:
            if " - " in para.text:
                quote = QuoteModel(*para.text.strip().split(" - "))
                quotes.append(quote)

        return quotes
