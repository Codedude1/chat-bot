import os
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFaceHub

class AngelOneChatbot:
    def __init__(self):
        # Use MiniLM for embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'batch_size': 4}
        )

        # Load vector DB (already persisted on disk)
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )

        # Use Hugging Face hosted LLM
        self.llm = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",  # Or any supported model
            model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
        )

        # QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True
        )

    def query(self, question):
        try:
            result = self.qa_chain.invoke({"query": question})
            if not result.get("result") or "I don't know" in result["result"]:
                return "I Don't know"
            return result["result"]
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I Don't know"
