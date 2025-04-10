#!/bin/bash

echo "📦 Extracting PDFs..."
unzip -o pdfs/Insurance\ PDFs.zip -d pdfs/

echo "🔍 Running data processing..."
python3 data_processing.py

echo "🧠 Building vector database..."
python3 vector_db.py

echo "🚀 Starting Flask app..."
python3 app.py
