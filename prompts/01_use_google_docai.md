  > Instead of Google Cloud Vision API, investigate the use of Google Document AI which seems a better option for this task. https://cloud.google.com/document-ai/docs/overview  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

✦ You are right to point out Google Document AI. It is indeed a more powerful and suitable tool for this specific task. While the Vision API is great for general-purpose image analysis, Document
  AI is specialized for extracting structured information from documents, including handwritten text, which makes it a better choice for processing homework sheets.

  Here is the plan to integrate Google Document AI:


   1. Install the Client Library: You will need to install the Google Cloud Document AI library.
   2. Create a Document AI Processor: You will need to create a processor in your Google Cloud project. For this use case, a "Form Parser" or a custom processor would be ideal. You will need the
      Project ID and Processor ID from the Google Cloud Console.
   3. Update the Backend Code: I will modify backend/main.py to use the Document AI client library, sending the image to your new processor and parsing the structured response.

  First, please install the necessary library by running this command in your activated backend virtual environment:


   1 pip install google-cloud-documentai



  Next, you will need to create a processor in the Google Cloud Console (https://console.cloud.google.com/ai/document-ai/processors). A good starting point is the Form Parser processor, as it
  is quite versatile. Once created, make a note of your Project ID and the Processor ID.


  After you have installed the library and have your credentials ready, I will proceed with updating the Python code. Shall I continue?