# Automated Proposal Generator

A production-ready, full-stack B2B tool that automates the creation of technical project proposals. The system ingests client requirement PDFs, retrieves context from a RAG-based SQLite database of past projects, uses Gemini AI to generate a structured proposal, and calculates deterministic pricing. 

It features a robust FastAPI backend for intelligent processing and a premium, dark-mode "Mission Control" Next.js frontend with real-time terminal-style status logging.

## Features

*   **PDF Requirement Parsing:** Automatically extracts requirements and context from client-provided PDF documents.
*   **AI-Powered Proposal Generation:** Leverages Google's Gemini AI to craft professional, structured, and highly relevant technical proposals.
*   **RAG Context Retrieval:** Uses Retrieval-Augmented Generation with an SQLite database of past projects to ensure proposals are grounded in historical company data and capabilities.
*   **Deterministic Pricing Engine:** Calculates accurate and reliable project pricing based on extracted requirements.
*   **Mission Control Dashboard:** A sleek, premium dark-mode Next.js frontend providing an intuitive user experience.
*   **Real-time Processing Logs:** Terminal-style logging in the UI to give users live visibility into the backend proposal generation process.

## Tech Stack

**Frontend:**
*   Next.js (React)
*   TypeScript
*   Tailwind CSS (Premium Dark Mode UI)

**Backend:**
*   FastAPI (Python)
*   SQLite (RAG Database)
*   Google Gemini AI API

## Prerequisites

*   Node.js (v18+)
*   Python (3.9+)
*   Google Gemini API Key

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Sainiashmit/Automated-Proposal-Generator.git
cd Automated-Proposal-Generator
```

### 2. Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install dependencies (ensure your terminal is in the backend folder):
    ```bash
    pip install fastapi uvicorn google-generativeai pypdf2 python-multipart
    ```
4.  Set up your environment variables by creating a `.env` file in the `backend` directory:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
5.  Initialize the database:
    ```bash
    python init_db.py
    ```
6.  Start the FastAPI server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### 3. Frontend Setup

1.  Open a new terminal window and navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the Next.js development server:
    ```bash
    npm run dev
    ```

The frontend will be accessible at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## Project Structure

```text
Automated-Proposal-Generator/
├── backend/                # FastAPI backend application
│   ├── main.py             # API entry point
│   ├── ai_generator.py     # Gemini AI integration
│   ├── pdf_processor.py    # PDF parsing logic
│   ├── db_query.py         # Database query & RAG logic
│   ├── pricing_engine.py   # Deterministic pricing logic
│   └── init_db.py          # Database initialization
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   └── components/     # Reusable UI components
│   ├── package.json
│   └── ...
└── README.md
```