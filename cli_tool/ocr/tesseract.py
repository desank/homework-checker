import logging
from PIL import Image
import pytesseract
from .base import OcrProcessor

class TesseractProcessor(OcrProcessor):
    def __init__(self):
        logging.info("Initializing Tesseract OCR processor.")
        # You might want to add a check here to ensure tesseract is installed and in PATH
        # For example, by trying to get its version: pytesseract.get_tesseract_version()

    def process_image(self, image_path: str) -> str:
        logging.info(f"Processing image with Tesseract: {image_path}")
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            logging.error(f"An error occurred with Tesseract: {e}")
            return ""
