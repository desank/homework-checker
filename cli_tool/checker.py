import argparse
import re
import sys
from google.cloud import documentai
from google.api_core import exceptions
from google.auth import exceptions as auth_exceptions
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: Replace with your GCP project details
PROJECT_ID = "agentverse-fgyga"
LOCATION = "us"  # e.g., "us" or "eu"
PROCESSOR_ID = "65dfc50dd803238"

def evaluate_expression(expr):
    logging.info(f"Evaluating expression: {expr}")
    try:
        # More robust sanitization for handwritten text
        sanitized_expr = re.sub(r'[^0-9+\-*/.=]', '', expr)
        logging.info(f"Sanitized expression: {sanitized_expr}")
        
        if '=' not in sanitized_expr:
            logging.warning("No '=' sign found in expression.")
            return None, None, None

        parts = sanitized_expr.split('=', 1)
        if len(parts) != 2:
            logging.warning("Expression does not have a clear question and answer.")
            return None, None, None

        question, answer = parts
        
        # Avoid evaluating empty strings
        if not question.strip() or not answer.strip():
            logging.warning("Empty question or answer.")
            return None, None, None
            
        # Evaluate the question part
        logging.info(f"Evaluating: {question}")
        correct_answer = eval(question)
        logging.info(f"Correct answer: {correct_answer}")
        
        # Compare with the provided answer
        is_correct = float(answer) == float(correct_answer)
        logging.info(f"Student answer: {answer}, Correct: {is_correct}")
        return is_correct, correct_answer, float(answer)

    except (SyntaxError, NameError, ZeroDivisionError, ValueError) as e:
        # Catch evaluation errors
        logging.error(f"Could not evaluate expression: {expr}. Error: {e}")
        return None, None, None

def process_image(image_path):
    logging.info("Starting image processing.")
    try:
        # Instantiates a client
        opts = {"api_endpoint": f"{LOCATION}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        logging.info("Document AI client created.")

        # The full resource name of the processor
        name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        logging.info(f"Processor path: {name}")

        # Read the file content
        logging.info(f"Reading image file: {image_path}")
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        logging.info("Image file read successfully.")
        
        # Load Binary Data into Document AI RawDocument object
        raw_document = documentai.RawDocument(
            content=image_data,
            mime_type="image/jpeg",  # Assuming JPEG, adjust if needed
        )
        logging.info("Raw document created.")

        # Configure the process request
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        logging.info("Process request configured.")

        # Use the Document AI client to process the document
        logging.info("Sending request to Document AI...")
        result = client.process_document(request=request)
        document = result.document
        logging.info("Document AI processing complete.")
        
        return document.text

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
        return None

def main():
    try:
        parser = argparse.ArgumentParser(description="Check math homework from a scanned image.")
        parser.add_argument("image_path", help="The path to the scanned image file.")
        args = parser.parse_args()

        logging.info(f"Processing {args.image_path}...")
        extracted_text = process_image(args.image_path)

        if not extracted_text:
            logging.error("Could not extract text from the image.")
            return

        print("\n--- Extracted Text ---")
        print(extracted_text)
        print("----------------------\n")

        lines = extracted_text.strip().split('\n')
        
        correct_count = 0
        total_count = 0

        print("--- Homework Results ---")
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            is_correct, correct_answer, student_answer = evaluate_expression(line)

            if is_correct is not None:
                total_count += 1
                if is_correct:
                    correct_count += 1
                    print(f"Question {total_count}: {line} ... CORRECT")
                else:
                    print(f"Question {total_count}: {line} ... INCORRECT (Correct answer is {correct_answer})")
            else:
                # Try to be more intelligent about what is a math expression
                if '=' in line and any(c in '+-*/' for c in line):
                     print(f"Could not evaluate: {line}")


        print("\n--- Summary ---")
        if total_count > 0:
            percentage = (correct_count / total_count) * 100
            print(f"Score: {correct_count}/{total_count} ({percentage:.2f}%) ")
        else:
            print("No valid math expressions found to evaluate.")

    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
