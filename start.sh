#!/bin/bash

echo "Running pre-start scripts..."

# Run vector prep
python3 data_processing.py
python3 vector_db.py

echo "Starting Flask app..."
python3 app.py
