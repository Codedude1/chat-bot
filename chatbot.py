from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Together
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

class AngelOneChatbot:
    def __init__(self):
        # Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )

        # Vector DB
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )

        # LLM from Together.ai
        self.llm = Together(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.2,
            max_tokens=512,
            together_api_key=os.getenv("TOGETHER_API_KEY")
        )

        # Stricter prompt
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant. Use only the context below to answer the question.
If the answer is not in the context, respond with "I Don't know".

Context:
{context}

Question: {question}

Strict Answer:"""
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question):
        try:
            result = self.qa_chain.invoke({"query": question})
            source_docs = result.get("source_documents", [])
            answer = result.get("result", "").strip()

            # Log retrieved docs
            for i, doc in enumerate(source_docs):
                print(f"\n🔍 Retrieved [Doc {i+1}]:\n{doc.page_content[:300]}\n")

            if not source_docs or "i don't know" in answer.lower():
                return "I Don't know"
            return answer
        except Exception as e:
            print(f"Error: {e}")
            return "I Don't know"
