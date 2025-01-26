import argparse
import os
import shutil
from tqdm import tqdm
from langchain_community.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from chromadb.utils import embedding_functions
import chromadb

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    """Main function coordinating document processing and database operations"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--query", type=str, help="Query the database.")
    args = parser.parse_args()

    # Step 1: Database Reset (if requested)
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Step 2: Initialize ChromaDB
    print("💾 Initializing ChromaDB at:", CHROMA_PATH)
    embeddings = embedding_functions.DefaultEmbeddingFunction()
    db = initialize_chroma(embeddings)

    # Step 3: Handle Query or Process Documents
    if args.query:
        print("🔎 Running Query:", args.query)
        results = db.query(
            query_texts=[args.query],
            n_results=45
        )
        print_results(results)
    else:
        # Step 4: Load and Process Documents
        print("📂 Loading documents from:", DATA_PATH)
        documents = load_documents()
        print(f"✅ Loaded {len(documents)} documents.")

        print("🔄 Splitting documents into chunks...")
        chunks = split_documents(documents)
        print(f"✅ Split into {len(chunks)} chunks.")

        print("🆕 Adding documents to ChromaDB...")
        add_to_chroma(db, chunks)
        print("✅ Done!")

def initialize_chroma(embeddings):
    """Initialize or get existing ChromaDB collection"""
    client = chromadb.PersistentClient(path="./chroma")
    try:
        collection = client.get_collection(name="my_collection")
    except:
        collection = client.create_collection(
            name="my_collection", 
            embedding_function=embeddings
        )
    return collection

def load_documents():
    """Load all txt documents from the DATA_PATH directory"""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data directory not found at: {DATA_PATH}")
    
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    return loader.load()

def split_documents(documents: list[Document]):
    """Split documents into smaller chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=320,  # Smaller chunks for better embedding
        chunk_overlap=60,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    return calculate_chunk_ids(chunks)

def calculate_chunk_ids(chunks):
    """Generate unique IDs for each chunk based on source and index"""
    last_source_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        current_source_id = source

        if current_source_id == last_source_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_source_id}:{current_chunk_index}"
        last_source_id = current_source_id
        chunk.metadata["id"] = chunk_id

    return chunks

def add_to_chroma(collection, chunks: list[Document]):
    """Add document chunks to ChromaDB collection"""
    for chunk in tqdm(chunks, desc="Adding chunks"):
        collection.add(
            documents=[chunk.page_content],
            ids=[chunk.metadata["id"]],
            metadatas=[chunk.metadata]
        )

def print_results(results):
    """Print query results in a formatted way"""
    print("\n🔍 Top Results:")
    if results['documents'][0]:
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
            print(f"\n{i}. Content:")
            print(f"{doc}")
            print(f"Metadata: {metadata}")
    else:
        print("No results found.")
    print()

def clear_database():
    """Clear the ChromaDB database"""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"🗑️ Database cleared at: {CHROMA_PATH}")
    else:
        print("⚠️ Database not found. Nothing to clear.")

def query_search(query_text: str):
    """
    Search the database with a query string.
    Args:
        query_text (str): The text to search for
    """
    # Initialize ChromaDB
    embeddings = embedding_functions.DefaultEmbeddingFunction()
    db = initialize_chroma(embeddings)
    
    # Run query
    print("🔎 Running Query:", query_text)
    results = db.query(
        query_texts=[query_text],  # Note: needs to be a list
        n_results=15
    )
    
    # Print formatted results
    print_results(results)
    return str(results)


if __name__ == "__main__":
    main()