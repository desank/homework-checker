import logging
from .base import OcrProcessor

class Pix2TextProcessor(OcrProcessor):
    def __init__(self):
        logging.info("Initializing Pix2Text processor.")
        from pix2text import Pix2Text
        self.p2t = Pix2Text()

    def process_image(self, image_path: str) -> str:
        logging.info(f"Processing image with Pix2Text: {image_path}")
        try:
            outs = self.p2t(image_path)
            # The output from pix2text is a list of dicts, each with 'type' and 'content'.
            # We will join the content of all detected elements.
            content_list = [item['content'] for item in outs]
            return "\n".join(content_list)
        except Exception as e:
            logging.error(f"An error occurred with Pix2Text: {e}")
            return ""

