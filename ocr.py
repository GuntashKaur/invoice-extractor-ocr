from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from config import *

POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"

def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        pages = convert_from_path(
            file_path,
            poppler_path=POPPLER_PATH   # 🔥 FORCE PATH
        )

        for i, page in enumerate(pages):
            temp_path = f"temp/page_{i}.jpg"
            page.save(temp_path, "JPEG")
            text += pytesseract.image_to_string(Image.open(temp_path)) + "\n"

    else:
        text = pytesseract.image_to_string(Image.open(file_path))

    return text