# 📺 YouTube Video Summarizer (RAG-Powered)

This application allows users to provide a YouTube URL, index its content into a vector database, and then ask questions about the video. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate answers based solely on the video transcript.

---

## 🚀 How It Works (The Architecture)

The system is built on a "Three-Pillar" architecture: **Extraction**, **Storage**, and **Retrieval**.

### 1. Extraction & Processing
* **Transcript Fetching:** The backend uses `youtube-transcript-api` to pull the text and timestamps from the video.
* **Recursive Chunking:** To fit into the AI's context window, the text is split using `RecursiveCharacterTextSplitter`. We use a **1,000-character size** with a **200-character overlap** to ensure context is preserved across chunks.

### 2. Vector Storage (The "Memory")
* **Embedding Model:** We use Google's `text-embedding-004` model. It converts text chunks into **768-dimension** numerical vectors.
* **Vector Database:** **Qdrant** stores these vectors. We use **Cosine Similarity** to find chunks based on semantic meaning rather than just keyword matches.
* **Lifespan Management:** The FastAPI app uses a `lifespan` event to ensure the Qdrant collection is created with the correct 768-dimension configuration the moment the server starts.

### 3. Retrieval-Augmented Generation (RAG)
* **Retrieval:** When you ask a question, the system converts your query into a vector and searches Qdrant for the top relevant transcript chunks.
* **Augmentation:** Those chunks are injected into a prompt as "Context."
* **Generation:** **Gemini 1.5 Flash** reads the context and your question to generate a precise answer.



---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ (Managed via `uv`) |
| **Framework** | FastAPI |
| **LLM & Embeddings** | Google Gemini API (Flash & text-embedding-004) |
| **Vector DB** | Qdrant (Running via Docker) |
| **Orchestration** | LangChain (`langchain-qdrant` partner package) |
| **Frontend** | React |

---

## 🏃 Getting Started

### 1. Prerequisites
* **Docker**: To run the Qdrant engine.
* **uv**: For high-speed Python package management.
* **Google AI Studio API Key**: To access Gemini and Embedding models.

### 2. Setup Environment
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=youtube_rag

3. Launch Services

Start the Qdrant vector database:
Bash

docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

Install dependencies and start the backend:
Bash

uv sync
uv run uvicorn main:app --reload

📡 API Endpoints

    POST /index: Accepts a video_url. Downloads transcript → Chunks text → Stores in Qdrant.

    POST /ask: Accepts a question. Retrieves relevant chunks → Generates answer using Gemini.

⚠️ Troubleshooting & Limits

    429 Resource Exhausted: You've hit the Gemini Free Tier limit. Wait 60 seconds. Using gemini-1.5-flash provides higher limits than pro models.

    Connection Refused: Ensure your Qdrant Docker container is running and accessible at localhost:6333.

    Dimension Mismatch: If you change embedding models, you must delete the existing Qdrant collection and let the lifespan event recreate it.

    TypeError (embeddings vs embedding): The modern langchain-qdrant package uses the singular embedding= argument in the constructor.


Would you like me to add a section explaining how to run the React frontend alongside this backend?