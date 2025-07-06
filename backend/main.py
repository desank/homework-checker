from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
import re
from google.cloud import documentai

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# TODO: Replace with your GCP project details
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us"  # e.g., "us" or "eu"
PROCESSOR_ID = "your-processor-id"

def evaluate_expression(expr):
    try:
        # Sanitize expression: remove any characters that are not digits, operators, or '='
        sanitized_expr = re.sub(r'[^0-9+\-*/.=]', '', expr)
        
        if '=' not in sanitized_expr:
            return False, 0

        parts = sanitized_expr.split('=', 1)
        if len(parts) != 2:
            return False, 0

        question, answer = parts
        
        # Avoid evaluating empty strings
        if not question.strip() or not answer.strip():
            return False, 0
            
        # Evaluate the question part
        correct_answer = eval(question)
        
        # Compare with the provided answer
        return float(answer) == float(correct_answer), correct_answer
    except (SyntaxError, NameError, ZeroDivisionError, ValueError):
        # Catch evaluation errors
        return False, 0

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Instantiates a client
        opts = {"api_endpoint": f"{LOCATION}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # The full resource name of the processor
        name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

        # Read the file content
        image_data = await file.read()
        
        # Load Binary Data into Document AI RawDocument object
        raw_document = documentai.RawDocument(
            content=image_data,
            mime_type=file.content_type,  # e.g., "image/jpeg" or "image/png"
        )

        # Configure the process request
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)

        # Use the Document AI client to process the document
        result = client.process_document(request=request)
        document = result.document
        
        text = document.text
        print("Extracted OCR Text:")
        print(text)

    except Exception as e:
        print(f"An error occurred with Document AI: {e}")
        raise HTTPException(status_code=500, detail="Error processing document with Document AI")

    lines = text.strip().split('\n')
    
    results = []
    correct_count = 0
    
    for line in lines:
        if not line.strip():
            continue
            
        is_correct, correct_answer = evaluate_expression(line)
        if is_correct:
            correct_count += 1
        
        results.append({
            "expression": line,
            "is_correct": is_correct,
            "correct_answer": correct_answer
        })
        
    return {
        "correct_count": correct_count,
        "total_count": len(results),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)