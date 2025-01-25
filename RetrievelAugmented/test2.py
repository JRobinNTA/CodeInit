import argparse
import os
import shutil
from tqdm import tqdm
from langchain_community.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import chromadb

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    print("📂 Loading documents from:", DATA_PATH)
    documents = load_documents()
    print(f"✅ Loaded {len(documents)} documents.")

    print("🔄 Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks.")

    print("💾 Initializing ChromaDB at:", CHROMA_PATH)
    add_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",  # Load only .txt files
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}  # Specify encoding for text files
    )
    return loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    # Initialize embedding function
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Initialize persistent ChromaDB client
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )

    # Initialize Chroma Vectorstore
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Add chunks to the database
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")

        with tqdm(total=len(new_chunks), desc="Adding Chunks to Chroma") as pbar:
            for chunk in new_chunks:
                new_chunk_id = chunk.metadata["id"]
                db.add_documents([chunk], ids=[new_chunk_id])
                db.persist()
                pbar.update(1)

    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
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


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
