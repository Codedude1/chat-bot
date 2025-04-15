import os
import tempfile
from bs4 import BeautifulSoup
from langchain_community.document_loaders import (
    BSHTMLLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from playwright.sync_api import sync_playwright

def scrape_angelone_support():
    base_url = "https://www.angelone.in/support"
    scraped_docs = []

    print("🔍 Launching headless browser to scrape support page...")
    try:
        with sync_playwright() as p:
            # Use a viewport size that simulates a desktop browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            
            # Add user agent to appear as a standard browser
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })
            
            print(f"Navigating to {base_url}...")
            page.goto(base_url, timeout=30000)  # Increased timeout
            
            # Wait for content to load fully
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(5000)  # Wait 5 seconds for any delayed JavaScript
            
            # Try the original selector first
            original_links = page.query_selector_all('a[href^="/support/"]')
            full_links = list(set(
                "https://www.angelone.in" + link.get_attribute("href")
                for link in original_links if link.get_attribute("href")
            ))
            
            # If original selector finds no links, try alternative selectors
            if not full_links:
                print("No links found with original selector, trying alternatives...")
                support_links = []
                
                # Look for various link patterns that might exist on the support page
                selectors = [
                    'a[href*="/support"]',  # Contains /support anywhere in href
                    'a[href*="faq"]',       # Contains faq anywhere in href
                    '.support-container a', '.faq-container a',  # Common container classes
                    '.card a', '.support-card a', '.faq-card a',  # Common card structures
                ]
                
                for selector in selectors:
                    try:
                        elements = page.query_selector_all(selector)
                        print(f"Selector '{selector}' found {len(elements)} elements")
                        
                        for element in elements:
                            href = element.get_attribute("href")
                            if href:
                                # Clean and normalize URL
                                if not href.startswith("http"):
                                    if href.startswith("/"):
                                        href = f"https://www.angelone.in{href}"
                                    else:
                                        href = f"https://www.angelone.in/{href}"
                                
                                # Only include Angel One links
                                if "angelone.in" in href:
                                    support_links.append(href)
                    except Exception as e:
                        print(f"Error with selector '{selector}': {e}")
                
                # Remove duplicates
                full_links = list(set(support_links))
            
            print(f"🔗 Found {len(full_links)} support links")
            
            # Print a sample of links for debugging
            for link in full_links[:5]:
                print(f"  - {link}")
            
            if len(full_links) > 5:
                print(f"  - ... and {len(full_links) - 5} more")
            
            # If we still don't have links, try to at least scrape the main support page
            if not full_links:
                print("No links found. Scraping main support page only...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
                    tmp.write(page.content())
                    tmp_path = tmp.name
                
                try:
                    loader = BSHTMLLoader(tmp_path)
                    main_docs = loader.load()
                    for doc in main_docs:
                        doc.metadata["source"] = base_url
                    scraped_docs.extend(main_docs)
                    print(f"✅ Scraped main support page")
                except Exception as e:
                    print(f"⚠️ Failed to scrape main support page: {e}")
            
            # Scrape individual support links
            for url in full_links:
                try:
                    page.goto(url, timeout=15000)
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(2000)  # Wait for dynamic content
                    
                    html = page.content()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
                        tmp.write(html)
                        tmp_path = tmp.name
                    
                    loader = BSHTMLLoader(tmp_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source"] = url
                    scraped_docs.extend(docs)
                    print(f"✅ Scraped: {url}")
                except Exception as e:
                    print(f"⚠️ Failed to scrape {url}: {e}")
            
            browser.close()
        
        print(f"📄 Total scraped web documents: {len(scraped_docs)}")
        return scraped_docs
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
                    print(f"✅ Loaded: {filepath}")
                except Exception as e:
                    print(f"⚠️ Error loading {filepath}: {e}")
            else:
                print(f"⛔ Skipping unsupported file: {filename}")
    return docs

def process_documents():
    print("📡 Scraping AngelOne support site...")
    web_docs = scrape_angelone_support()
    print("📂 Loading local documents from pdfs/ ...")
    local_docs = load_documents("pdfs")
    print(f"📄 Local docs loaded: {len(local_docs)}")

    all_docs = web_docs + local_docs
    print("✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(all_docs)
    print(f"📚 Created {len(splits)} document chunks")
    return splits
