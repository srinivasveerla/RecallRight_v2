import logging
import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from db_init import get_db
import PyPDF2

# Constants
CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Configure Logger
logger = logging.getLogger("RecallRight_v2")

def load_documents():
    """Load PDF documents from a specified directory."""
    logger.info("Loading documents from directory: %s", DATA_PATH)
    try:
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = document_loader.load()
        logger.info("Loaded %d documents.", len(documents))
        return documents
    except Exception as e:
        logger.error("Error loading documents: %s", e, exc_info=True)
        raise

def split_documents(documents: list[Document]):
    """Split documents into smaller chunks for processing."""
    logger.info("Splitting %d documents into chunks.", len(documents))
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info("Split documents into %d chunks.", len(chunks))
        return chunks
    except Exception as e:
        logger.error("Error splitting documents: %s", e, exc_info=True)
        raise

def calculate_chunk_ids(chunks):
    """Calculate unique chunk IDs based on metadata."""
    logger.info("Calculating unique chunk IDs for %d chunks.", len(chunks))
    last_page_id = None
    current_chunk_index = 0

    try:
        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # Update chunk index
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Assign chunk ID
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id
            chunk.metadata["id"] = chunk_id

        logger.info("Successfully calculated chunk IDs.")
        return chunks
    except Exception as e:
        logger.error("Error calculating chunk IDs: %s", e, exc_info=True)
        raise

def add_to_chroma(chunks: list[Document]):
    """Add chunks to ChromaDB, ensuring no duplicates."""
    logger.info("Adding chunks to ChromaDB.")
    try:
        db = get_db()
        chunks_with_ids = calculate_chunk_ids(chunks)

        # Get existing IDs in the DB
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        logger.info("Number of existing documents in DB: %d", len(existing_ids))

        # Identify new chunks
        new_chunks = []
        new_chunk_ids = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk.page_content)
                new_chunk_ids.append(chunk.metadata["id"])

        logger.info("New chunks to add: %d", len(new_chunks))
        if new_chunks:
            db.add(documents=new_chunks, ids=new_chunk_ids)
            db.client.persist()
            logger.info("Successfully added new chunks to ChromaDB.")
        else:
            logger.info("No new documents to add.")
    except Exception as e:
        logger.error("Error adding chunks to ChromaDB: %s", e, exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting document processing pipeline.")
    try:
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)
        logger.info("Document processing pipeline completed successfully.")
    except Exception as e:
        logger.critical("Pipeline execution failed: %s", e, exc_info=True)
