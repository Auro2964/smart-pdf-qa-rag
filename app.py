import os
import re
from io import BytesIO

import streamlit as st
from pypdf import PdfReader
from google import genai

st.set_page_config(page_title="Smart PDF Q&A", page_icon="📄", layout="wide")

st.title("📄 Smart PDF Question-Answering System")
st.caption("Ask questions about your PDFs using retrieval-augmented generation (RAG).")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Gemini API key",
        type="password",
        help="Your key is used only for this session. Never paste it into your source code or GitHub."
    )
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")
    st.info("Upload a PDF, then ask a question about its contents.")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

def extract_pages(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": page_number, "text": text})
    return pages

def chunk_pages(pages, chunk_size=1200, overlap=200):
    chunks = []
    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({"page": page["page"], "text": chunk_text})
            if end == len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks

def retrieve_chunks(question, chunks, limit=4):
    words = set(re.findall(r"[a-zA-Z0-9]{3,}", question.lower()))
    scored = []
    for chunk in chunks:
        chunk_words = set(re.findall(r"[a-zA-Z0-9]{3,}", chunk["text"].lower()))
        score = len(words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [chunk for score, chunk in scored[:limit] if score > 0]
    return selected or chunks[:min(limit, len(chunks))]

if uploaded_file:
    try:
        pages = extract_pages(uploaded_file.getvalue())
        chunks = chunk_pages(pages)
        if not chunks:
            st.warning("No selectable text was found. This PDF may be scanned; OCR is not included in this starter version.")
        else:
            st.success(f"Loaded **{uploaded_file.name}** — extracted text from {len(pages)} page(s) and created {len(chunks)} chunk(s).")
            with st.expander("Preview extracted text"):
                st.write(pages[0]["text"][:2500])

            question = st.text_input("Ask a question about this document", placeholder="Example: What are the main findings?")
            if st.button("Get answer", type="primary", disabled=not question.strip()):
                if not api_key.strip():
                    st.error("Enter your Gemini API key in the sidebar first.")
                else:
                    selected = retrieve_chunks(question, chunks)
                    context = "\n\n".join(
                        f"[PDF page {item['page']}]\n{item['text']}" for item in selected
                    )
                    prompt = f"""You answer questions using only the provided PDF excerpts.
If the excerpts do not contain the answer, say that the document does not provide enough information.
Do not invent facts. Cite the relevant PDF page number(s) in your answer.

PDF EXCERPTS:
{context}

QUESTION:
{question}

Answer clearly and include page references."""
                    try:
                        client = genai.Client(api_key=api_key.strip())
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        st.subheader("Answer")
                        st.write(response.text or "The model returned an empty response.")
                        st.subheader("Retrieved source excerpts")
                        for item in selected:
                            with st.expander(f"PDF page {item['page']}"):
                                st.write(item["text"])
                    except Exception as exc:
                        st.error("The request failed. Check your API key, internet connection, model availability, and API quota.")
                        st.caption(f"Technical detail: {exc}")
    except Exception as exc:
        st.error("Could not read this PDF. Try another text-based PDF.")
        st.caption(f"Technical detail: {exc}")
else:
    st.markdown("""
    ### How to use
    1. Add your Gemini API key in the sidebar.
    2. Upload a text-based PDF.
    3. Type a question and click **Get answer**.
    4. Review the answer and the retrieved page excerpts.

    **How it works:** PDF text extraction → overlapping text chunks → keyword-based retrieval → Gemini answer grounded in the selected excerpts.
    """)
    st.warning("This is a portfolio starter project. It uses simple keyword retrieval rather than a vector database, and scanned PDFs need OCR.")
