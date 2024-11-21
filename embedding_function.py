import logging
from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from get_genai import get_genai

# Initialize the logger
logger = logging.getLogger("RecallRight_v2")

# Ensure logger propagation
logger.propagate = True

# Get the genai instance
genai = get_genai()


class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    def __init__(self):
        logger.info("Initializing GeminiEmbeddingFunction with document_mode=%s", self.document_mode)

    def __call__(self, input: Documents) -> Embeddings:
        logger.debug("Embedding function called with input: %s", input)

        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        logger.info("Selected embedding task: %s", embedding_task)

        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
        try:
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=input,
                task_type=embedding_task,
                request_options=retry_policy,
            )
            logger.info("Embedding generated successfully for input.")
            return response["embedding"]
        except Exception as e:
            logger.error("Failed to generate embedding: %s", e, exc_info=True)
            raise
