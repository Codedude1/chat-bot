#!/bin/bash

echo "🛠 Starting Setup..."

echo "🌍 Installing Playwright browsers..."
playwright install

echo "📥 Downloading Insurance PDFs from Google Drive..."
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1KYUaU7J2NL6TSHMIGTJ3QeWQLx7d_GQ8' -O Insurance_PDFs.zip

echo "📂 Extracting PDFs..."
mkdir -p pdfs
unzip -o Insurance_PDFs.zip -d pdfs

echo "🧹 Cleaning unsupported files..."
find pdfs/ -type f ! -iname "*.pdf" ! -iname "*.docx" -delete

echo "⚙️ Creating Vector DB..."
python3 vector_db.py || echo "❌ Vector DB creation failed"

echo "🚀 Launching Flask app..."
python3 app.py
