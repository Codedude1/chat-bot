import os
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

class AngelOneChatbot:
    def __init__(self):
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'batch_size': 4}
        )
        
        
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        
        
        self.llm = OllamaLLM(model="mistral")
        
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True
        )
    
    def query(self, question):
        try:
            result = self.qa_chain.invoke({"query": question})
            
            
            if not result["source_documents"] or "I don't know" in result["result"]:
                return "I Don't know"
            
            return result["result"]
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I Don't know"
