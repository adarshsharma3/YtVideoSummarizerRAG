import { useState } from 'react'
import './App.css'

function App() {
  const [videoUrl, setVideoUrl] = useState('')
  const [question, setQuestion] = useState('')
  const [indexingStatus, setIndexingStatus] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const handleIndex = async () => {
    if (!videoUrl) return;
    setLoading(true);
    setIndexingStatus('Indexing video...');
    try {
      const response = await fetch('http://localhost:8000/index?video_url=' + encodeURIComponent(videoUrl), {
        method: 'POST',
      });
      const data = await response.json();
      if (response.ok) {
        setIndexingStatus(`Success: ${data.status}. Chunks: ${data.chunks}`);
      } else {
        setIndexingStatus('Error indexing video');
      }
    } catch (error) {
      console.error("Error indexing:", error);
      setIndexingStatus('Error connecting to server');
    }
    setLoading(false);
  };

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    setAnswer('Thinking...');
    try {
      const response = await fetch('http://localhost:8000/ask?question=' + encodeURIComponent(question), {
        method: 'POST',
      });
      const data = await response.json();
      if (response.ok) {
        setAnswer(data.answer);
      } else {
        setAnswer('Error getting answer');
      }
    } catch (error) {
      console.error("Error asking:", error);
      setAnswer('Error connecting to server');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>YouTube Video Q&A</h1>

      <div className="card">
        <h2>1. Index Video</h2>
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
          />
          <button onClick={handleIndex} disabled={loading}>
            {loading ? 'Processing...' : 'Index'}
          </button>
        </div>
        {indexingStatus && <p className="status">{indexingStatus}</p>}
      </div>

      <div className="card">
        <h2>2. Ask Question</h2>
        <div className="input-group">
          <input
            type="text"
            placeholder="Ask a question about the video"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleAsk} disabled={loading}>
            Ask
          </button>
        </div>
        {answer && (
          <div className="answer-box">
            <h3>Answer:</h3>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
