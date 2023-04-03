#Email Text Scraper

#import dependencies including pytesseract
from PIL import Image
import pytesseract

def textRead(path, language):
    im = Image.open(path)
    text = pytesseract.image_to_string(im)
    return text

