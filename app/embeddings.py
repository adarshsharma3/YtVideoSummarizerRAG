from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import GEMINI_API_KEY

def get_embeddings():
    # This returns the LangChain-compatible model object
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", # Latest, more stable model
        google_api_key=GEMINI_API_KEY,
        # Task type helps optimize for vector search
        task_type="retrieval_document" 
    )