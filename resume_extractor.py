import fitz
import pytesseract
import cv2
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path):

    text = ""

    if file_path.lower().endswith(".pdf"):

        doc = fitz.open(file_path)

        for page in doc:

            page_text = page.get_text()

            if page_text.strip():
                text += page_text

            else:
                pix = page.get_pixmap()

                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

                text += pytesseract.image_to_string(img)

    elif file_path.lower().endswith((".jpg", ".png", ".jpeg")):

        img = cv2.imread(file_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

    return text


# Run extractor directly
if __name__ == "__main__":

    file = "data"

    extracted_text = extract_text(file)

    print(extracted_text[:1000])