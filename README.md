# Smart PDF Question-Answering System (RAG)

A Streamlit application that lets a user upload a text-based PDF, ask a question, retrieve relevant excerpts, and generate an answer with Google Gemini. The answer is instructed to stay grounded in the retrieved excerpts and cite PDF page numbers.

> **Status:** Starter portfolio project. Test it with your own PDFs and document any issues before describing it as production-ready.

## Features

- Upload a PDF through the browser
- Extract selectable text and split it into overlapping chunks
- Retrieve relevant chunks using simple keyword overlap
- Generate a response using the Gemini API
- Display retrieved source excerpts and PDF page references
- Keep the API key out of the source code

## Technology stack

- Python
- Streamlit
- pypdf
- Google Gen AI SDK (Gemini)

## Project structure

```text
smart-pdf-qa-rag/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run locally

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
```

5. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

6. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
7. Run the app:

```bash
streamlit run app.py
```

8. Paste your key into the app's sidebar and upload a text-based PDF.

## How it works

1. **Extract:** `pypdf` extracts selectable text from each PDF page.
2. **Chunk:** Long page text is split into overlapping sections.
3. **Retrieve:** The app scores chunks by keyword overlap with the question and selects the top matches.
4. **Generate:** The selected excerpts and question are sent to Gemini.
5. **Review:** The answer and retrieved excerpts are shown so the user can inspect the supporting text.

## Limitations

- Scanned/image-only PDFs need OCR, which is not included.
- Retrieval uses keyword overlap, not embeddings or a vector database.
- Generated answers can still be incorrect; verify important information against the original PDF.
- API access, rate limits, model names, and pricing/quotas may change. Check the current Google AI Studio terms and availability.
- Do not upload confidential, personal, legal, medical, or client documents unless you have permission and have checked the provider's data-handling terms.

## Security

- Never commit API keys, passwords, private PDFs, or client data.
- `.env` and Streamlit secrets are ignored by Git.
- The app asks for the API key during the session and does not save it to the repository.

## Future improvements

- Replace keyword retrieval with embeddings and a vector database such as ChromaDB.
- Add tests for text extraction, chunking, and retrieval.
- Add OCR support for scanned documents.
- Add chat history and a more detailed evaluation set.

## Author

**Aurokalyan Sahoo**  
GitHub: [@auro2964](https://github.com/auro2964)  
LinkedIn: [Aurokalyan Sahoo](https://linkedin.com/in/auro-kalyan-sahoo)
