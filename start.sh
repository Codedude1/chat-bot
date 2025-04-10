#!/bin/bash

echo "🔄 Starting Setup..."

# 1. Install Playwright browsers (Render installs packages via requirements.txt but NOT browsers)
echo "🌐 Installing Playwright browsers..."
playwright install

# 2. Download and extract PDFs
echo "📥 Downloading Insurance PDFs from Google Drive..."
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1KYUaU7J2NL6TSHMIGTJ3QeWQLx7d_GQ8' -O Insurance_PDFs.zip

echo "📂 Extracting PDFs..."
mkdir -p pdfs
unzip -o Insurance_PDFs.zip -d pdfs

# Optional: Clean unsupported files
echo "🧹 Cleaning unsupported file types..."
find pdfs/ -type f ! -iname "*.pdf" ! -iname "*.docx" -delete

# 3. Process documents
echo "🧠 Running data processing..."
python3 data_processing.py || echo "⚠️ Data processing failed, check logs!"

# 4. Start the Flask app
echo "🚀 Launching Flask app..."
python3 app.py
