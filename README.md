# AI-Powered Math Homework Checker

This project is a web application designed to automatically check and grade math homework from a scanned image. It uses Google Cloud Document AI to extract handwritten mathematical expressions and then evaluates them to determine their correctness.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Configuration](#setup-and-configuration)
  - [1. Google Cloud Platform](#1-google-cloud-platform)
  - [2. Backend (FastAPI)](#2-backend-fastapi)
  - [3. Frontend (React)](#3-frontend-react)
  - [4. CLI Tool](#4-cli-tool)
- [Running the Application](#running-the-application)
  - [Running the Backend Server](#running-the-backend-server)
  - [Running the Frontend App](#running-the-frontend-app)
  - [Using the CLI Tool](#using-the-cli-tool)
- [How to Use](#how-to-use)

## Features

- **Image Upload:** Mobile-friendly web interface to upload a picture of a homework sheet.
- **OCR for Math:** Extracts handwritten text and mathematical problems using Google Document AI.
- **Automatic Grading:** Evaluates each mathematical expression to check if the answer is correct.
- **Instant Feedback:** Displays the results, highlighting incorrect answers and providing the correct solution.
- **CLI Interface:** Provides a command-line tool for power users to check homework directly from the terminal.

## Architecture

The application is composed of three main parts:

1.  **Frontend:** A single-page application built with **React** and styled with **Bootstrap**. It provides the user interface for uploading images and viewing results.
2.  **Backend:** A RESTful API built with **Python (FastAPI)**. It handles image uploads, interacts with the Google Document AI API to perform OCR, evaluates the extracted expressions, and returns the graded results.
3.  **AI Service:** **Google Cloud Document AI** is used as the core OCR engine, specifically chosen for its strength in parsing structured and handwritten text from documents.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js and npm](https://nodejs.org/en/)
- [Python 3.8+](https://www.python.org/downloads/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

## Setup and Configuration

Follow these steps to set up the project environment.

### 1. Google Cloud Platform

This project relies on the Google Document AI API.

1.  **Create a GCP Project:** If you don't have one already, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable Document AI API:** In your GCP project, navigate to the "APIs & Services" dashboard and enable the "Document AI API".
3.  **Create a Processor:** Go to the [Document AI processors page](https://console.cloud.google.com/ai/document-ai/processors) and create a new processor. The **Form Parser** is a good choice for this use case.
4.  **Note Your Credentials:** Make a note of your **Project ID**, **Processor ID**, and the **Location** (e.g., `us`, `eu`) of your processor.
5.  **Authenticate:** Authenticate your local environment so the application can access the API. Run the following command and follow the prompts:
    ```bash
    gcloud auth application-default login
    ```

### 2. Backend (FastAPI)

The backend server handles the core logic.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Update Configuration:** Open `backend/main.py` and replace the placeholder values for `PROJECT_ID`, `LOCATION`, and `PROCESSOR_ID` with your GCP credentials noted in the previous step.

    ```python
    # backend/main.py
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "your-processor-location" # e.g., "us"
    PROCESSOR_ID = "your-processor-id"
    ```

### 3. Frontend (React)

The frontend is the user-facing web application.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

### 4. CLI Tool

The project also includes a standalone command-line tool.

1.  **Navigate to the cli_tool directory:**
    ```bash
    cd cli_tool
    ```
2.  **Install dependencies:** The CLI tool shares dependencies with the backend. If you have already set up the backend's virtual environment, you can use that. Otherwise, install the required package:
    ```bash
    pip install google-cloud-documentai
    ```
3.  **Update Configuration:** Open `cli_tool/checker.py` and replace the placeholder values for `PROJECT_ID`, `LOCATION`, and `PROCESSOR_ID` with your GCP credentials.

    ```python
    # cli_tool/checker.py
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "your-processor-location" # e.g., "us"
    PROCESSOR_ID = "your-processor-id"
    ```

## Running the Application

### Running the Backend Server

From the `backend` directory (with the virtual environment activated):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API server will be running at `http://localhost:8000`.

### Running the Frontend App

From the `frontend` directory (in a new terminal):

```bash
npm start
```

This will open the web application in your default browser at `http://localhost:3000`.

### Using the CLI Tool

From the root directory (with the backend virtual environment activated):

```bash
python cli_tool/checker.py path/to/your/homework.jpg
```

For example:
```bash
python cli_tool/checker.py test/kumon1.jpg
```

## How to Use

-   **Web App:**
    1.  Navigate to `http://localhost:3000`.
    2.  Click the "Upload a picture of the homework" button and select an image file.
    3.  The results will be displayed automatically below the upload button, showing the score and highlighting any incorrect answers.

-   **CLI Tool:**
    1.  Run the command from your terminal, providing the path to the image.
    2.  The tool will output the extracted text, the evaluation of each problem, and a final summary score.
