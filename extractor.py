from ocr import extract_text
from parser import extract_fields
import os

def process_invoice(file_path):
    text = extract_text(file_path)

    # ✅ FIX: convert list → string
    if isinstance(text, list):
        text = "\n".join(text)

    data = extract_fields(text)

     # invoice type
    file_ext = os.path.splitext(file_path)[1].lower().replace(".", "")
    data["invoice_type"] = file_ext
    return data