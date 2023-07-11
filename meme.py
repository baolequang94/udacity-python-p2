from QuoteEngine.model import QuoteModel
from QuoteEngine import Ingestor
from MemeEngine import MemeEngine
from pathlib import Path
import os
import random
import argparse


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='To generate a meme.')
    parser.add_argument('--body', type=str, help="Quote's body")
    parser.add_argument('--author', type=str, help="Quote's author")
    parser.add_argument('--path', type=Path, help="Path to image for using")

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
