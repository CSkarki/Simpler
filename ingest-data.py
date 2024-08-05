
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import openai


OPENAI_API_KEY = "sk-proj-nE9wV4kdhjBAFxaFo7uDT3BlbkFJrTUhJnzVbMVhBvqfTgeH"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

#DATA_SOURCE_PATH = "/source_data"
CHROMA_PATH = "data/chroma"


def load_documents(DataSourcePath):
    DirectoryLoader = PyPDFDirectoryLoader(DataSourcePath)
    return (DirectoryLoader.load())

   # for doc in Documents:
    #    print(doc.metadata)
    #split_doc = split_documents(Documents)

    #for splitdoc in split_doc:
    #    print(splitdoc)


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)
    for chunk in chunks:
        print(f"Chunk Page Sample: {chunk.metadata['id']}\n{chunk.page_content}\n\n")

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        return len(new_chunks)
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the chunk meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks




