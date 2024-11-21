import chromadb
from embedding_function import GeminiEmbeddingFunction

def get_db():
    DB_NAME = "googlecardb"
    embed_fn = GeminiEmbeddingFunction()
    embed_fn.document_mode = True
    PERSIST_DIR = "./chroma_db_store"

    chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
    db = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=embed_fn)
    return db