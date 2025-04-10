from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import AngelOneChatbot

app = Flask(__name__)
CORS(app)


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
    app.run(host='0.0.0.0', port=5000)
