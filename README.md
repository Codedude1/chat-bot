# AngelOne Chatbot (RAG-based)

This repository contains the code for a Retrieval-Augmented Generation (RAG) chatbot that answers queries based solely on the provided AngelOne support documents and PDFs.

The project uses:
- **Web Scraping:** Using Playwright and BeautifulSoup to scrape the AngelOne support website.
- **PDF/DOCX Processing:** Using LangChain’s document loaders.
- **Embeddings:** Generated via HuggingFace’s `all-MiniLM-L6-v2` model.
- **Vector Store:** Chroma vector store for efficient retrieval.
- **LLM:** HuggingFaceHub (Mistral-7B-Instruct-v0.1) for answer generation with a strict prompt.
- **Backend:** Flask with CORS enabled.

A live demo is available at:  
[AngelOne Chatbot (Vercel)](https://v0-rag-chatbot-development.vercel.app/)

---

## Prerequisites

- Python 3.9 or higher
- [Playwright](https://playwright.dev/python/docs/intro) (browsers need to be installed with `playwright install`)
- A valid HuggingFace API token (set as `HUGGINGFACEHUB_API_TOKEN` in your environment)

---

## Local Setup Instructions

1. **Clone the Repository:**

   ```bash
     git clone https://github.com/Codedude1/chat-bot.git
     cd chat-bot
2. **Create a Virtual Environment and Activate It:**

    ```bash
     python3 -m venv venv
     source venv/bin/activate
3. **Install Dependencies**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install "huggingface_hub[hf_xet]" unstructured numpy==1.26.4 playwright
    playwright install chromium
4. **Prepare the Data:**

    - Place your Insurance PDFs and DOCX files in the pdfs/ directory.

    - The project will also scrape the AngelOne support website for additional content.

5. **Build the Vector Store**

    ```bash
    python data_processing.py
    python vector_db.py

6. **Run the Flask App:**
  ```bash
  python app.py

```
The backend will be live at localhost: 5000.

7. **Test the Chatbot via cURL:**

    ```
    curl -X POST http://127.0.0.1:5000/chat \
    -H "Content-Type: application/json" \
    -d '{"question": "What is covered under life insurance?"}'

If the chatbot does not have sufficient context, it will respond with “I Don't know.”

