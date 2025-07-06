import argparse
import re
import sys
import logging
from paddleocr import PaddleOCR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaddleOcrProcessor:
    def __init__(self):
        logging.info("Initializing PaddleOCR processor.")
        self.ocr = PaddleOCR(use_textline_orientation=True, lang='en')

    def process_image(self, image_path):
        logging.info(f"Running OCR on {image_path}")
        result = self.ocr.ocr(image_path)  # Removed cls=True as it's not supported
        # Extract text lines from result
        lines = []
        for line in result:
            for box in line:
                lines.append(box[1][0])
        return '\n'.join(lines)

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

def main():
    try:
        parser = argparse.ArgumentParser(description="Check math homework from a scanned image.")
        parser.add_argument("image_path", help="The path to the scanned image file.")
        args = parser.parse_args()

        print("Initializing the OCR engine. This may take a few moments on the first run...")
        ocr_processor = PaddleOcrProcessor()

        logging.info(f"Processing {args.image_path}...")
        extracted_text = ocr_processor.process_image(args.image_path)

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
