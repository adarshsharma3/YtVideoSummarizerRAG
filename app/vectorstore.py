from qdrant_client import QdrantClient,models
# from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore as Qdrant
from app.config import QDRANT_URL, COLLECTION_NAME
from app.embeddings import get_embeddings

client = QdrantClient(url=QDRANT_URL)
embeddings = get_embeddings()

def ensure_collection():
    # Check if collection exists, if not, create it
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    if not exists:
        print(f"Creating collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=768, # Size for text-embedding-004
                distance=models.Distance.COSINE
            )
        )

def store_chunks(chunks: list[str]):
    Qdrant.from_texts(
        texts=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )

def get_vectorstore():
    return Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
