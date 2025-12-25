from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.transcript import get_transcript
from app.chunker import chunk_text
from app.vectorstore import store_chunks, ensure_collection # Add ensure_collection
from app.mainRag import answer_query

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    print("Checking Vector Database...")
    ensure_collection() 
    yield
    print("Closing connections... Goodbye!")
    # This runs when the server shuts down (if needed)

app = FastAPI(title="YouTube RAG Q&A", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/index")
def index_video(video_url: str):
    transcript = get_transcript(video_url)
    chunks = chunk_text(transcript)
    store_chunks(chunks)
    return {"status": "Video indexed successfully", "chunks": len(chunks)}

@app.post("/ask")
def ask_question(question: str):
    answer = answer_query(question)
    return {"answer": answer}
