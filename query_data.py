import logging
from db_init import get_db
from get_genai import get_genai

# Constants
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Configure Logger
logger = logging.getLogger("RecallRight_v2")

def main():
    """Main function to handle user queries."""
    logger.info("Starting query handling process.")
    try:
        query_text = input("Enter your query:\n")
        context_text, ids = query_vectordb(query_text)
        logger.info("Relevant context fetched successfully.")
        call_llm(context_text, ids, query_text)
    except Exception as e:
        logger.critical("Error in main function: %s", e, exc_info=True)

def query_vectordb(query_text: str):
    """Query the vector database and retrieve relevant context."""
    logger.info("Querying the vector database for: %s", query_text)
    try:
        db = get_db()
        results = db.query(query_texts=[query_text], n_results=3)

        # Extract documents and IDs
        [docs] = results["documents"]
        [ids] = results["ids"]
        context_text = "".join(docs)

        logger.info("Retrieved %d relevant documents.", len(docs))
        return context_text, ids
    except Exception as e:
        logger.error("Error querying vector database: %s", e, exc_info=True)
        raise

def call_llm(context_text, ids, query_text):
    """Invoke the LLM with context and query text."""
    logger.info("Calling the LLM with provided context and query.")
    try:
        # Format prompt
        passage_oneline = context_text.replace("\n", " ")
        query_oneline = query_text.replace("\n", " ")
        prompt = f"""You are a helpful and informative bot that answers questions using text from the reference passage included below. 
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and 
        strike a friendly and conversational tone. If the passage is irrelevant to the answer, you may ignore it.

        QUESTION: {query_oneline}
        PASSAGE: {passage_oneline}
        """

        # Generate response
        genai = get_genai()
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        answer = model.generate_content(prompt)
        logger.info("LLM response generated successfully.")

        # Display result
        logger.info("Response: %s", answer.text)
        print(answer.text)
    except Exception as e:
        logger.error("Error invoking LLM: %s", e, exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting the application.")
    try:
        main()
        logger.info("Application completed successfully.")
    except Exception as e:
        logger.critical("Application terminated with errors: %s", e, exc_info=True)
