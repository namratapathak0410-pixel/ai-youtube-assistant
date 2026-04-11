from langchain_openai import ChatOpenAI
from src.config.settings import OPENAI_API_KEY
from src.vectorstore.faiss_store import FAISSStore

store = FAISSStore()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)

def build_index(chunks):
    store.add(chunks)

def ask(query):
    results = store.search(query)
    context = " ".join(results)

    prompt = f"""
    You are a helpful tutor.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)
    return response.content