import { useState } from 'react'
import './App.css'

// Mock data - replace with actual API response
const mockStatements = [
  {
    id: 1,
    statement: "The Earth is approximately 4.5 billion years old, based on radiometric age dating of meteorite material.",
    factScore: 95,
    source: "Scientific consensus",
    timestamp: "0:45"
  },
  {
    id: 2,
    statement: "Water covers about 71% of the Earth's surface, with oceans holding 96.5% of all Earth's water.",
    factScore: 98,
    source: "USGS",
    timestamp: "1:23"
  },
  {
    id: 3,
    statement: "The Great Wall of China is visible from space with the naked eye.",
    factScore: 15,
    source: "NASA debunked",
    timestamp: "2:10"
  },
  {
    id: 4,
    statement: "Humans share approximately 60% of their DNA with bananas.",
    factScore: 72,
    source: "Partially accurate",
    timestamp: "3:45"
  },
  {
    id: 5,
    statement: "Lightning never strikes the same place twice.",
    factScore: 8,
    source: "Common myth",
    timestamp: "4:30"
  }
]

function App() {
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  const [statements, setStatements] = useState([])
  const [hasAnalyzed, setHasAnalyzed] = useState(false)

  const validateYouTubeUrl = (url) => {
    const patterns = [
      /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=[\w-]+/,
      /^(https?:\/\/)?(www\.)?youtube\.com\/shorts\/[\w-]+/,
      /^(https?:\/\/)?youtu\.be\/[\w-]+/,
      /^(https?:\/\/)?(www\.)?youtube\.com\/embed\/[\w-]+/,
    ]
    return patterns.some(pattern => pattern.test(url))
  }

  const getInputState = () => {
    if (!url) return ''
    return validateYouTubeUrl(url) ? 'valid' : 'error'
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'high'
    if (score >= 50) return 'medium'
    return 'low'
  }

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Verified'
    if (score >= 50) return 'Partially True'
    return 'Misleading'
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!url.trim()) {
      setMessage({ type: 'error', text: 'Please enter a YouTube URL' })
      return
    }

    if (!validateYouTubeUrl(url)) {
      setMessage({ type: 'error', text: 'Please enter a valid YouTube URL' })
      return
    }

    setIsLoading(true)
    setMessage({ type: '', text: '' })
    setStatements([])

    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000))

      setStatements(mockStatements)
      setHasAnalyzed(true)
      setMessage({ type: 'success', text: `Found ${mockStatements.length} statements to analyze` })
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to analyze. Please try again.' })
    } finally {
      setIsLoading(false)
    }
  }

  const averageScore = statements.length > 0
    ? Math.round(statements.reduce((acc, s) => acc + s.factScore, 0) / statements.length)
    : 0

  return (
    <div className="container">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" fill="none" stroke="currentColor" strokeWidth="2" />
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" fill="none" stroke="currentColor" strokeWidth="2" />
              <circle cx="12" cy="12" r="3" fill="currentColor" />
            </svg>
          </div>
          <span className="logo-text">Investigator</span>
        </div>
        <p className="tagline">Analyze YouTube videos with AI-powered insights</p>
      </header>

      <div className="card">
        <h2 className="card-title">Submit a Video</h2>
        <p className="card-subtitle">Paste a YouTube URL to start the investigation</p>

        <form className="url-form" onSubmit={handleSubmit}>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
            </svg>
            <input
              type="text"
              className={`url-input ${getInputState()}`}
              placeholder="https://youtube.com/watch?v=..."
              value={url}
              onChange={(e) => {
                setUrl(e.target.value)
                setMessage({ type: '', text: '' })
              }}
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            className="submit-btn"
            disabled={isLoading || !url.trim()}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8" />
                  <path d="m21 21-4.35-4.35" />
                </svg>
                Investigate
              </>
            )}
          </button>
        </form>

        {message.text && (
          <div className={`message ${message.type}`}>
            {message.type === 'error' ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            )}
            {message.text}
          </div>
        )}
      </div>

      {/* Results Section */}
      {hasAnalyzed && statements.length > 0 && (
        <div className="results-section">
          {/* Summary Card */}
          <div className="summary-card">
            <div className="summary-header">
              <h3>Analysis Summary</h3>
              <span className="statement-count">{statements.length} statements</span>
            </div>
            <div className="summary-stats">
              <div className="stat-item">
                <div className={`overall-score ${getScoreColor(averageScore)}`}>
                  <span className="score-value">{averageScore}</span>
                  <span className="score-max">/100</span>
                </div>
                <span className="stat-label">Overall Credibility</span>
              </div>
              <div className="stat-breakdown">
                <div className="breakdown-item">
                  <span className="breakdown-dot high"></span>
                  <span className="breakdown-count">{statements.filter(s => s.factScore >= 80).length}</span>
                  <span className="breakdown-label">Verified</span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-dot medium"></span>
                  <span className="breakdown-count">{statements.filter(s => s.factScore >= 50 && s.factScore < 80).length}</span>
                  <span className="breakdown-label">Partial</span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-dot low"></span>
                  <span className="breakdown-count">{statements.filter(s => s.factScore < 50).length}</span>
                  <span className="breakdown-label">Misleading</span>
                </div>
              </div>
            </div>
          </div>

          {/* Statements List */}
          <div className="statements-section">
            <h3 className="section-title">Extracted Statements</h3>
            <div className="statements-list">
              {statements.map((item, index) => (
                <div key={item.id} className="statement-card" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className="statement-header">
                    <span className="timestamp">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="12 6 12 12 16 14" />
                      </svg>
                      {item.timestamp}
                    </span>
                    <div className={`fact-badge ${getScoreColor(item.factScore)}`}>
                      <span className="badge-score">{item.factScore}</span>
                      <span className="badge-label">{getScoreLabel(item.factScore)}</span>
                    </div>
                  </div>

                  <p className="statement-text">{item.statement}</p>

                  <div className="statement-footer">
                    <div className="score-bar-container">
                      <div
                        className={`score-bar ${getScoreColor(item.factScore)}`}
                        style={{ width: `${item.factScore}%` }}
                      ></div>
                    </div>
                    <span className="source-tag">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" y1="14" x2="21" y2="3" />
                      </svg>
                      {item.source}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <p>Supports YouTube videos, Shorts, and embedded links</p>
      </footer>
    </div>
  )
}

export default App
