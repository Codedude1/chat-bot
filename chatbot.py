from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

class AngelOneChatbot:
    def __init__(self):
        # Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'batch_size': 4}
        )

        # Load vector store
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )

        # LLM with slightly higher temperature for some variability (adjust as needed)
        self.llm = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",
            model_kwargs={"temperature": 0.2, "max_new_tokens": 512}
        )

        # Strict prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant. Use only the context below to answer the question.
If the answer is not in the context, respond with "I Don't know" and do not fabricate any answer.

Context:
{context}

Question: {question}
Helpful Answer:"""
        )

        # RetrievalQA with strict prompt, with an increased number of retrieved documents
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
            # Debug: Log how many documents were retrieved
            print("Debug: Retrieved", len(source_docs), "source documents.")
            for i, doc in enumerate(source_docs):
                print(f"Doc {i+1} snippet: {doc.page_content[:300]}")
            answer = result.get("result", "").strip()
            # If no context or if answer contains "i don't know", return fallback.
            if not source_docs or "i don't know" in answer.lower():
                return "I Don't know"
            return answer
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I Don't know"
