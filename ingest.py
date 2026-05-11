import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "mohenjo_daro_kb"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_documents():
    documents = []
    for file_path in DATA_DIR.glob("*.txt"):
        if file_path.name == "resources.txt":
            continue
        print(f"Loading {file_path.name}...")
        loader = TextLoader(str(file_path))
        docs = loader.load()
        for doc in docs:
            doc.metadata["category"] = file_path.stem
            doc.metadata["source"] = file_path.name
        documents.extend(docs)
    print(f"Loaded {len(documents)} documents")
    return documents

def split_documents(documents):
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks

def create_vector_store(chunks):
    if CHROMA_DIR.exists():
        print("Removing existing ChromaDB...")
        import shutil
        shutil.rmtree(CHROMA_DIR)

    print(f"Creating embeddings with {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print("Storing in ChromaDB...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )
    print(f"Vector store created with {vector_store.count()} documents")
    return vector_store

def main():
    print("=" * 50)
    print("MOHENJO-DARO KNOWLEDGE BASE INGESTION")
    print("=" * 50)

    documents = load_documents()
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)

    print("=" * 50)
    print("INGESTION COMPLETE")
    print(f"Database location: {CHROMA_DIR.absolute()}")
    print("=" * 50)

if __name__ == "__main__":
    main()
