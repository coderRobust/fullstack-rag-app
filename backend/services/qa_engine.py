"""
Service to run the RAG Q&A pipeline using LangChain.
"""

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from core.config import settings  # or from core.settings if that's your file


async def get_answer(question: str) -> str:
    try:
        print("🔍 Loading FAISS index...")
        db = FAISS.load_local(
            "faiss_index",
            OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY),
            allow_dangerous_deserialization=True
        )

        print("Performing similarity search...")
        docs = db.similarity_search(question, k=4)

        print("Generating answer...")
        llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY)
        chain = load_qa_chain(llm, chain_type="stuff")

        return chain.run(input_documents=docs, question=question)

    except Exception as e:
        print("Error in RAG pipeline:", str(e))
        return "Error generating answer"
