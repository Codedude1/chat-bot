#!/bin/bash

echo "🔄 Starting Setup..."

# 1. Download and extract PDFs
echo "📦 Downloading Insurance PDFs from Google Drive..."
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1KYUaU7J2NL6TSHMIGTJ3QeWQLx7d_GQ8' -O Insurance_PDFs.zip

echo "📂 Extracting PDFs..."
mkdir -p pdfs
unzip -o Insurance_PDFs.zip -d pdfs

# 2. Process documents
echo "🧠 Running data processing..."
python3 data_processing.py

# 3. Build vector DB
echo "🧱 Creating vector database..."
python3 vector_db.py

# 4. Start app
echo "🚀 Starting Flask app..."
python3 app.py
