from QuoteEngine.model import QuoteModel
from QuoteEngine import Ingestor
from MemeEngine import MemeEngine
from flask import Flask, render_template, request
from pathlib import Path
import os
import random
import requests
import tempfile
from requests.packages import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
current_dir = Path(__file__).parent
meme = MemeEngine('./static')


def setup():
    """Setup loading all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []

    for quote_file in quote_files:
        print(quote_file)
        quotes += Ingestor.parse(quote_file)
        print(Ingestor.parse(quote_file))

    images_path = "./_data/photos/dog/"

    imgs = []
    for file in os.listdir(images_path):
        if file.endswith(".jpg"):
            imgs.append(os.path.join(images_path, file))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img, quote = (random.choice(item) for item in (imgs, quotes))
    out_path = meme.make_meme(img, quote)
    return render_template('meme.html', path=Path(out_path).relative_to(current_dir))


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme creation."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""

    try:
        image_url = request.form.get("image_url")
        res = requests.get(image_url, verify=False)

        tmp_d, tmp_img = tempfile.mkstemp(
            dir=current_dir, prefix="tmp-img", suffix=".png")
        with open(tmp_img, 'wb') as tmp_f:
            tmp_f.write(res.content)

        body = request.form.get("body")
        author = request.form.get("author")
        quote = QuoteModel(body, author)
        output_path = meme.make_meme(tmp_img, quote)
        os.close(tmp_d)
        os.remove(tmp_img)
    except:
        print("Bad Image")
        return render_template('meme_form.html')

    return render_template('meme.html', path=Path(output_path).relative_to(current_dir))


if __name__ == "__main__":
    app.run()
