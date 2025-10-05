import { useState, useEffect, useRef } from 'react'

/**
 * FirePreventionChatbot component
 * - Provides a chat interface for fire prevention questions
 * - Integrates with Gemini AI backend
 * - Maintains conversation history
 */
export default function FirePreventionChatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load welcome message when chatbot opens
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      loadWelcomeMessage()
    }
  }, [isOpen])

  const loadWelcomeMessage = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/chatbot/welcome')
      const data = await response.json()
      
      if (data.success) {
        setMessages([{
          id: Date.now(),
          role: 'assistant',
          content: data.message,
          timestamp: data.timestamp,
          isWelcome: true
        }])
      } else {
        setError(data.error || 'Failed to load welcome message')
      }
    } catch (err) {
      setError('Failed to connect to chatbot service')
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    }

    // Add user message immediately
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:5001/api/chatbot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_history: messages.map(msg => ({
            role: msg.role,
            content: msg.content
          }))
        })
      })

      const data = await response.json()

      if (data.success) {
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.message,
          timestamp: data.timestamp
        }
        setMessages(prev => [...prev, assistantMessage])
      } else {
        setError(data.error || 'Failed to get response')
      }
    } catch (err) {
      setError('Failed to send message')
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    setError(null)
    if (isOpen) {
      loadWelcomeMessage()
    }
  }

  return (
    <>
      {/* Chatbot Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="chatbot-toggle"
        aria-label="Open fire prevention chatbot"
      >
        🔥 Fire Safety Assistant
      </button>

      {/* Chatbot Modal */}
      {isOpen && (
        <div className="chatbot-modal">
          <div className="chatbot-header">
            <h3>🔥 Fire Prevention Assistant</h3>
            <div className="chatbot-controls">
              <button onClick={clearChat} className="clear-btn" title="Clear chat">
                🗑️
              </button>
              <button onClick={() => setIsOpen(false)} className="close-btn" title="Close chat">
                ✕
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role} ${message.isWelcome ? 'welcome' : ''}`}
              >
                <div className="message-content">
                  {message.content.split('\n').map((line, idx) => (
                    <p key={idx}>{line}</p>
                  ))}
                </div>
                <div className="message-timestamp">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant loading">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            {error && (
              <div className="message error">
                <div className="message-content">
                  <p>❌ {error}</p>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={sendMessage} className="chatbot-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask about fire prevention..."
              disabled={isLoading}
              autoFocus
            />
            <button type="submit" disabled={!inputMessage.trim() || isLoading}>
              {isLoading ? '⏳' : '📤'}
            </button>
          </form>
        </div>
      )}

      <style jsx>{`
        .chatbot-toggle {
          position: fixed;
          bottom: 20px;
          right: 20px;
          background: linear-gradient(135deg, #ff6b35, #f7931e);
          color: white;
          border: none;
          border-radius: 25px;
          padding: 12px 20px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
          transition: all 0.3s ease;
          z-index: 1000;
        }

        .chatbot-toggle:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(255, 107, 53, 0.4);
        }

        .chatbot-modal {
          position: fixed;
          bottom: 80px;
          right: 10px;
          width: 320px;
          height: 400px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          display: flex;
          flex-direction: column;
          z-index: 1001;
          border: 1px solid #e0e0e0;
        }

        .chatbot-header {
          background: linear-gradient(135deg, #ff6b35, #f7931e);
          color: white;
          padding: 16px;
          border-radius: 12px 12px 0 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .chatbot-header h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
        }

        .chatbot-controls {
          display: flex;
          gap: 8px;
        }

        .clear-btn, .close-btn {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          width: 28px;
          height: 28px;
          border-radius: 50%;
          cursor: pointer;
          font-size: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background 0.2s;
        }

        .clear-btn:hover, .close-btn:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .chatbot-messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .message {
          display: flex;
          flex-direction: column;
          max-width: 85%;
        }

        .message.user {
          align-self: flex-end;
        }

        .message.assistant {
          align-self: flex-start;
        }

        .message-content {
          background: #f5f5f5;
          padding: 12px 16px;
          border-radius: 18px;
          font-size: 14px;
          line-height: 1.4;
          color: #000;
        }

        .message.user .message-content {
          background: linear-gradient(135deg, #ff6b35, #f7931e);
          color: #000;
        }

        .message.welcome .message-content {
          background: linear-gradient(135deg, #4CAF50, #45a049);
          color: #000;
          font-weight: 500;
        }

        .message.error .message-content {
          background: #ffebee;
          color: #c62828;
          border: 1px solid #ffcdd2;
        }

        .message-content p {
          margin: 0 0 8px 0;
        }

        .message-content p:last-child {
          margin-bottom: 0;
        }

        .message-timestamp {
          font-size: 11px;
          color: #666;
          margin-top: 4px;
          padding: 0 4px;
        }

        .typing-indicator {
          display: flex;
          gap: 4px;
          align-items: center;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: #999;
          border-radius: 50%;
          animation: typing 1.4s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
          }
          30% {
            transform: translateY(-10px);
            opacity: 1;
          }
        }

        .chatbot-input {
          display: flex;
          padding: 16px;
          border-top: 1px solid #e0e0e0;
          gap: 8px;
        }

        .chatbot-input input {
          flex: 1;
          padding: 12px 16px;
          border: 1px solid #ddd;
          border-radius: 20px;
          font-size: 14px;
          outline: none;
          transition: border-color 0.2s;
        }

        .chatbot-input input:focus {
          border-color: #ff6b35;
        }

        .chatbot-input button {
          background: linear-gradient(135deg, #ff6b35, #f7931e);
          color: white;
          border: none;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          cursor: pointer;
          font-size: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.2s;
        }

        .chatbot-input button:hover:not(:disabled) {
          transform: scale(1.05);
        }

        .chatbot-input button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* Responsive design */
        @media (max-width: 480px) {
          .chatbot-modal {
            width: calc(100vw - 20px);
            height: calc(100vh - 120px);
            bottom: 10px;
            right: 10px;
          }
          
          .chatbot-toggle {
            bottom: 15px;
            right: 15px;
          }
        }
      `}</style>
    </>
  )
}
