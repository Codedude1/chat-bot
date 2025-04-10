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

        # LLM
        self.llm = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",
            model_kwargs={"temperature": 0.0, "max_new_tokens": 512}
        )

        # Strict prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant. Use only the context below to answer the question.

If the answer is not in the context, just respond with "I Don't know".

Context:
{context}

Question: {question}
Helpful Answer:"""
        )

        # RetrievalQA with strict prompt
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question):
        try:
            result = self.qa_chain.invoke({"query": question})
            answer = result.get("result", "").strip()

            if not result.get("source_documents") or "i don't know" in answer.lower():
                return "I Don't know"
            return answer
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I Don't know"
