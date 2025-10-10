"""
Author: Rohini
Email: rolearnings@yahoo.com
Date: 2025-10-10
Description: This script intened to have chat from the UI using streamlit
"""
            

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

def get_data_chunks(text_file_path: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    
    try:
        loader = TextLoader(text_file_path)
        docs = loader.load()
    except Exception as e:
        print(f"Unable to load the text data {text_file_path} due to error {e}")
    
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(docs)
        return chunks
    except Exception as e:
        print(f"Unable to chunk the data !! {e}")

def get_embeddings():
    """
    Generate embeddings with transformers

    Returns:
        _type_: _description_
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return embeddings
    except Exception as e:
        print(f"Unable to embed the data {e}")

def store_data(chunks: list, embeddings: object, storage_dir: str) -> any:
    """
    Store embeddings to vector DB
    "chroma_db"

    Args:
        chunks (list): _description_
        embeddings (object): _description_
        storage_dir (str): _description_

    Returns:
        str: _description_
    """
    try:
        db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=storage_dir)
        db.persist()
        return db
    except Exception as e:
        print(f"Unable to store the data in Vector DB {e}")

if __name__ == "__main__":
    text_file_path = "data/staging_data/Sri-Sai-Satcharitra-English.txt"
    chunk_size = 5000
    chunk_overlap = 100
    
    chunks = get_data_chunks(text_file_path=text_file_path, \
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embeddings = get_embeddings()
    db = store_data(chunks, embeddings, "chroma_db")
    
    llm = Ollama(model="mistral")

    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Ask a question
    question = "Who was Shama in Sai Satcharitra?"
    answer = qa_chain.run(question)
    print(answer)



