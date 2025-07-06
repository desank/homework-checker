import sys
import logging
from google.cloud import documentai
from google.api_core import exceptions
from google.auth import exceptions as auth_exceptions
from .base import OcrProcessor

class GoogleDocAiProcessor(OcrProcessor):
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id

    def process_image(self, image_path: str) -> str:
        logging.info("Starting image processing with Google Document AI.")
        try:
            opts = {"api_endpoint": f"{self.location}-documentai.googleapis.com"}
            client = documentai.DocumentProcessorServiceClient(client_options=opts)
            name = client.processor_path(self.project_id, self.location, self.processor_id)

            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            raw_document = documentai.RawDocument(
                content=image_data,
                mime_type="image/jpeg",
            )

            request = documentai.ProcessRequest(name=name, raw_document=raw_document)
            result = client.process_document(request=request)
            return result.document.text

        except FileNotFoundError:
            logging.error(f"Image file not found at: {image_path}")
            sys.exit(1)
        except auth_exceptions.RefreshError as e:
            logging.critical(f"Authentication failed: {e}")
            logging.critical("This is likely a permission error. Please check your GCP credentials and permissions.")
            sys.exit(1)
        except exceptions.ServiceUnavailable as e:
            logging.critical(f"Service Unavailable: {e.message}")
            logging.critical("This is likely a permission error. Please check your GCP credentials.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"An error occurred with Document AI: {e}")
            return ""
