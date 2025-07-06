I have another idea. Create a new folder in this project named cli_tool. In that folder, I want to create a CLI program as per following prompt. I want to create a software program that     │
│    takes a scanned image of a bunch of maths questions answered by a 11 year student. And I want to check the correctness of the answers. Make sure you incorporate support for handwriting      │
│    recognition too. An example of one such quantum answer sheet scanned can be found @test/kumon1.jpg. I was thinking of the Rust programming language but feel free to use any other language   │
│    that’s more suitable for such cli program. Write such a CLI program that uses Google document AI api. @test/kumon1.jpg            

Ans:

 I have created the checker.py script in the cli_tool directory.

  Before you can run it, you need to:


   1. Install the required library:

   1     pip install google-cloud-documentai

   2. Set up authentication:

   1     gcloud auth application-default login

   3. Fill in your project details: Open cli_tool/checker.py and replace the placeholder values for PROJECT_ID, LOCATION, and PROCESSOR_ID with your Google Cloud project information.

  To run the CLI tool:


  Once you have completed the setup, you can run the homework checker from your terminal like this:


   1 python cli_tool/checker.py test/kumon1.jpg



  This will process the image, print the extracted text, and show you the results of the homework evaluation.
