
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Important for Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)

        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img) + "\n"

    else:
        text = pytesseract.image_to_string(Image.open(file_path))

    return text