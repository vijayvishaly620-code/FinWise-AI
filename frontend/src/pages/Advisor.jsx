import React, { useState, useEffect, useRef } from 'react'
import { advisor } from '../services/api'
import { Bot, Send, Activity, TrendingUp, Heart, Loader } from 'lucide-react'

export default function Advisor() {
  const [activeTab, setActiveTab] = useState('chat')
  const [analysis, setAnalysis] = useState(null)
  const [health, setHealth] = useState(null)
  const [predictions, setPredictions] = useState(null)
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hi! I\'m your FinWise AI advisor. Ask me anything about your finances, or click "Analyze My Finances" to get a full report.' }
  ])
  const [input, setInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      const data = await advisor.analyze()
      setAnalysis(data)
    } catch (err) {
      setAnalysis({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  const handleHealth = async () => {
    setLoading(true)
    try {
      const data = await advisor.getHealth()
      setHealth(data)
    } catch (err) {
      setHealth({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  const handlePredict = async () => {
    setLoading(true)
    try {
      const data = await advisor.predictExpenses()
      setPredictions(data)
    } catch (err) {
      setPredictions({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  const handleChat = async (e) => {
    e.preventDefault()
    if (!input.trim() || chatLoading) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setChatLoading(true)
    try {
      const data = await advisor.chat(userMsg)
      setMessages(prev => [...prev, { role: 'bot', content: data.response || data.message || 'I couldn\'t process that request.' }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: 'Sorry, I encountered an error. Please try again.' }])
    } finally {
      setChatLoading(false)
    }
  }

  const getHealthColor = (score) => {
    if (score >= 80) return 'var(--success)'
    if (score >= 60) return 'var(--warning)'
    return 'var(--danger)'
  }

  const getHealthLabel = (score) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Fair'
    return 'Needs Attention'
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>AI Financial Advisor</h2>
          <p>Get personalized insights and recommendations</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {[
          { id: 'chat', label: 'Chat', icon: <Bot size={16} /> },
          { id: 'analysis', label: 'Full Analysis', icon: <Activity size={16} /> },
          { id: 'health', label: 'Health Score', icon: <Heart size={16} /> },
          { id: 'predictions', label: 'Predictions', icon: <TrendingUp size={16} /> },
        ].map(tab => (
          <button key={tab.id} className={`btn ${activeTab === tab.id ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab(tab.id)}>
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'chat' && (
        <div className="card">
          <div className="chat-container">
            <div className="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`chat-message ${msg.role}`}>{msg.content}</div>
              ))}
              {chatLoading && <div className="chat-message bot"><Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> Thinking...</div>}
              <div ref={chatEndRef} />
            </div>
            <form className="chat-input" onSubmit={handleChat}>
              <input type="text" value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about your finances..." disabled={chatLoading} />
              <button type="submit" className="btn btn-primary btn-sm" disabled={chatLoading || !input.trim()}><Send size={16} /></button>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'analysis' && (
        <div>
          <button className="btn btn-primary" onClick={handleAnalyze} disabled={loading} style={{ marginBottom: 16 }}>
            {loading ? 'Analyzing...' : 'Run Full Analysis'}
          </button>
          {analysis && !analysis.error ? (
            <div className="card">
              <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Financial Analysis</h3>
              {analysis.summary && <p style={{ color: 'var(--text-secondary)', marginBottom: 16, lineHeight: 1.7 }}>{analysis.summary}</p>}
              {analysis.advice && (
                <div className="advice-list">
                  {(Array.isArray(analysis.advice) ? analysis.advice : [analysis.advice]).map((item, i) => {
                    const severity = item.severity || item.priority || 'info'
                    return (
                      <div key={i} className={`advice-item ${severity}`}>
                        <div>
                          <h4>{item.title || item.heading || `Recommendation ${i + 1}`}</h4>
                          <p>{item.message || item.text || item.content || JSON.stringify(item)}</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
              {analysis.scores && (
                <div style={{ marginTop: 20 }}>
                  <h4 style={{ marginBottom: 12 }}>Scores</h4>
                  {Object.entries(analysis.scores).map(([key, val]) => (
                    <div key={key} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                      <span style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</span>
                      <span style={{ fontWeight: 600 }}>{typeof val === 'number' ? `${val}/100` : val}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : analysis?.error && (
            <div className="card" style={{ borderColor: 'var(--danger)' }}>
              <p style={{ color: 'var(--danger)' }}>{analysis.error}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'health' && (
        <div>
          <button className="btn btn-primary" onClick={handleHealth} disabled={loading} style={{ marginBottom: 16 }}>
            {loading ? 'Calculating...' : 'Check Financial Health'}
          </button>
          {health && !health.error ? (
            <div className="card">
              <div className="health-score-display">
                <div className="score" style={{ color: getHealthColor(health.score) }}>{health.score}</div>
                <div className="out-of">out of 100</div>
                <div className="label" style={{ color: getHealthColor(health.score) }}>{getHealthLabel(health.score)}</div>
              </div>
              {health.details && (
                <div style={{ marginTop: 20 }}>
                  {health.details.map((d, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
                      <span>{d.category || d.name || `Item ${i + 1}`}</span>
                      <span style={{ fontWeight: 600 }}>{d.score || d.value}</span>
                    </div>
                  ))}
                </div>
              )}
              {health.tips && (
                <div style={{ marginTop: 20 }}>
                  <h4 style={{ marginBottom: 8 }}>Tips to Improve</h4>
                  {health.tips.map((tip, i) => (
                    <div key={i} className="advice-item info" style={{ marginBottom: 8 }}>
                      <p>{typeof tip === 'string' ? tip : tip.text || tip.message}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : health?.error && (
            <div className="card" style={{ borderColor: 'var(--danger)' }}>
              <p style={{ color: 'var(--danger)' }}>{health.error}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'predictions' && (
        <div>
          <button className="btn btn-primary" onClick={handlePredict} disabled={loading} style={{ marginBottom: 16 }}>
            {loading ? 'Predicting...' : 'Predict Next Month Expenses'}
          </button>
          {predictions && !predictions.error ? (
            <div className="card">
              <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Expense Predictions</h3>
              {predictions.predictions && (
                <div style={{ display: 'grid', gap: 8 }}>
                  {predictions.predictions.map((p, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border)' }}>
                      <span>{p.category}</span>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontWeight: 600 }}>${(p.predicted_amount || p.amount || 0).toLocaleString()}</div>
                        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Confidence: {p.confidence ? `${(p.confidence * 100).toFixed(0)}%` : 'N/A'}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              {predictions.total_predicted && (
                <div style={{ marginTop: 16, padding: '12px 0', borderTop: '2px solid var(--border)', display: 'flex', justifyContent: 'space-between', fontWeight: 600 }}>
                  <span>Total Predicted</span>
                  <span>${predictions.total_predicted.toLocaleString()}</span>
                </div>
              )}
            </div>
          ) : predictions?.error && (
            <div className="card" style={{ borderColor: 'var(--danger)' }}>
              <p style={{ color: 'var(--danger)' }}>{predictions.error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
