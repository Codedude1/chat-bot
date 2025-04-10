# data_processing.py
import os
import tempfile
from bs4 import BeautifulSoup
from langchain_community.document_loaders import (
    BSHTMLLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from playwright.sync_api import sync_playwright

def scrape_angelone_support():
    base_url = "https://www.angelone.in/support"
    print("🔍 Launching headless browser to scrape support page...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(base_url, timeout=15000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(5000)
            links = page.query_selector_all('a[href^="/support/"]')
            full_links = list(set(
                "https://www.angelone.in" + link.get_attribute("href")
                for link in links if link.get_attribute("href")
            ))
            print(f"🔗 Found {len(full_links)} support links")
            all_docs = []
            for url in full_links:
                try:
                    page.goto(url, timeout=10000)
                    html = page.content()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
                        tmp.write(html)
                        tmp_path = tmp.name
                    loader = BSHTMLLoader(tmp_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source"] = url
                    all_docs.extend(docs)
                    print(f"✅ Scraped: {url}")
                except Exception as e:
                    print(f"❌ Failed to scrape {url}: {e}")
            browser.close()
            print(f"📄 Total scraped web documents: {len(all_docs)}")
            return all_docs
    except Exception as e:
        print(f"❌ Error with Playwright scraping: {e}")
        return []

def load_documents(directory):
    docs = []
    loaders = {
        ".pdf": PyPDFLoader,
        ".docx": UnstructuredWordDocumentLoader,
    }
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in loaders:
                try:
                    loader = loaders[ext](filepath)
                    docs.extend(loader.load())
                    print(f"✅ Successfully loaded: {filepath}")
                except Exception as e:
                    print(f"❌ Error loading {filepath}: {e}")
            else:
                print(f"⚠️ Skipping unsupported file type: {filename}")
    return docs

def process_documents():
    print("📡 Scraping AngelOne support website...")
    web_docs = scrape_angelone_support()
    print("📂 Loading local documents from pdfs/ directory...")
    local_docs = load_documents("pdfs")
    print(f"📄 Total local docs loaded: {len(local_docs)}")
    all_docs = web_docs + local_docs
    print("✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(all_docs)
    print(f"📑 Processed {len(splits)} document chunks")
    print("📦 Saving documents to Chroma vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    vectorstore.persist() 
    print("✅ Chroma DB persisted successfully!")
    return splits
