#Email Text Scraper

#import dependencies including pytesseract
from PIL import Image
import pytesseract

def textRead(path, language):
    im = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(im)
    return text

print(textRead('uploads/image.png', 'eng'))