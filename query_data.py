import argparse
import chromadb
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from db_init import get_db
from embedding_function import GeminiEmbeddingFunction
from get_genai import get_genai
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()

    query_text = input("Enter your query:\n")
    context_text,ids = query_vectordb(query_text)
    print("Relevant data fetched:",context_text)
    call_llm(context_text,ids,query_text)


def query_vectordb(query_text: str):
    # Prepare the DB.
    db = get_db()

    # Search the DB.
    results = db.query(query_texts=[query_text], n_results=3)
    #print(results.keys())
    #context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    [docs] = results["documents"]
    print("Retrieved docs:",docs)
    [ids] = results["ids"]
    context_text = "".join(docs)
    return context_text,ids


def call_llm(context_text,ids,query_text):
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query_text)
    # # print(prompt)
    #
    # model = Ollama(model="mistral")
    # response_text = model.invoke(prompt)
    #
    # sources = [ids]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)
    # return response_text

    passage_oneline = context_text.replace("\n", " ")
    query_oneline = query_text.replace("\n", " ")

    prompt = f"""You are a helpful and informative bot that answers questions using text from the reference passage included below. 
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and 
    strike a friendly and converstional tone. If the passage is irrelevant to the answer, you may ignore it.

    QUESTION: {query_oneline}
    PASSAGE: {passage_oneline}
    """

    genai = get_genai()
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    answer = model.generate_content(prompt)
    print(answer)


if __name__ == "__main__":
    main()
