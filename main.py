import os
import glob
from typing import List
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

VECTOR_DB_PATH = "faiss_index"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

#fast api
app = FastAPI(title="RAG Chatbot")

# adding the vector store functions
def load_documents_from_path(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    return loader.load()


def build_vectorstore_from_file(file_path: str):
    docs = load_documents_from_path(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)
    return vectorstore

# it creates and loads the vector store
def load_or_create_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists(VECTOR_DB_PATH):
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    raise RuntimeError("No vectorstore found. Please call /load/ with a file first.")

# llm setup 
llm = ChatOpenAI(
    model_name="llama3-70b-8192",
    openai_api_key="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",
    openai_api_base="https://api.groq.com/openai/v1"
)

class FilePathRequest(BaseModel):
    file_path: str  # e.g., "sample.txt"

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

# endpoints
@app.post("/load/")
async def load_existing_file(input_data: FilePathRequest):
    file_path = input_data.file_path

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{file_path}' not found")

    try:
        build_vectorstore_from_file(file_path)
        return {"status": f"File '{file_path}' loaded and indexed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask")
def ask_question(query: QueryRequest):
    try:
        vectorstore = load_or_create_vectorstore()
    except RuntimeError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    retriever = vectorstore.as_retriever(search_kwargs={"k": query.top_k})
    docs = retriever.get_relevant_documents(query.question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Answer the question using the context below.\n\nContext:\n{context}\n\nQuestion: {query.question}"
    response = llm.invoke(prompt)
    return {"answer": response.content}
