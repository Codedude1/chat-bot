from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import AngelOneChatbot
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Verify the database has documents
if os.path.exists("./chroma_db"):
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vector_db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    print(f"Vector DB loaded with {vector_db._collection.count()} documents")
    if vector_db._collection.count() == 0:
        print("WARNING: Vector database is empty! Run vector_db.py first")
else:
    print("WARNING: Vector database not found! Run vector_db.py first")

chatbot = AngelOneChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = chatbot.query(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)