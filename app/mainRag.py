# import google.generativeai as genai
from app.config import GEMINI_API_KEY
from app.vectorstore import get_vectorstore

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)

# print(response.text)
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash")

def answer_query(question: str) -> str:
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
    Answer the question strictly using the context below.
    If the answer is not present, say "Not mentioned in the video".

    Context:
    {context}

    Question:
    {question}
    """

    # response = model.generate_content(prompt)

    response = client.models.generate_content(
    model="gemini-2.5-flash", contents={prompt}
    )
    return response.text
