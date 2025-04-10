import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from data_processing import process_documents

def create_vector_db():
    print("Processing documents...")
    documents = process_documents()
    print("Loading embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'batch_size': 1}
    )
    print("Creating vector database...")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    docs = vector_db.get()['documents']
    print("Total documents stored:", len(docs))
    vector_db.persist()
    print("✅ Vector database created successfully!")
    return vector_db

if __name__ == "__main__":
    os.system('clear')
    print("Starting vector database creation...")
    try:
        create_vector_db()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Run: pip install numpy==1.26.4 unstructured")
        print("2. Reduce document count if memory issues persist")
