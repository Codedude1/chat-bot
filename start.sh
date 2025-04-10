#!/bin/bash

echo "📁 Ensuring pdfs/ directory exists..."
mkdir -p pdfs

echo "📦 Extracting Insurance PDFs.zip into pdfs/..."
unzip -o "pdfs/Insurance PDFs.zip" -d pdfs/

echo "🧹 Cleaning up zipped file (optional)..."
rm -f "pdfs/Insurance PDFs.zip"

echo "📊 Running data processing..."
python3 data_processing.py || { echo "❌ Data processing failed"; exit 1; }

echo "🧠 Creating vector database..."
python3 vector_db.py || { echo "❌ Vector DB creation failed"; exit 1; }

echo "🚀 Launching Flask app..."
python3 app.py
