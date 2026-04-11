from langchain_openai import ChatOpenAI
from src.config.settings import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

def generate_questions(context):
    return llm.invoke(f"Generate 3 questions:\n{context}").content

def evaluate(q, a, context):
    prompt = f"Question: {q}\nAnswer: {a}\nContext:{context}\nEvaluate:"
    return llm.invoke(prompt).content