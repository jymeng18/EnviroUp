import { useState } from 'react'

/**
 * SearchBox component
 * - Renders an input and a button
 * - Sends the query to the backend via POST to /api/search (JSON: { q })
 * - Shows loading and error states and returns the response to the caller
 */
export default function SearchBox({ onResults, onSearchStart }) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    
    // Notify parent component that search started
    if (onSearchStart) onSearchStart()

    try {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
      const res = await fetch(`${apiBaseUrl}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: query }),
      })

      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)

      const data = await res.json()
      if (onResults) onResults(data)
    } catch (err) {
      setError(err.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="search"
          placeholder="Search for a location..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="search-input"
          aria-label="Search"
          disabled={loading}
        />
        <button 
          type="submit" 
          disabled={loading || !query.trim()} 
          className={`search-button ${loading ? 'loading' : ''}`}
        >
          {loading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <span>Searching...</span>
            </div>
          ) : (
            'Search'
          )}
        </button>
      </form>
      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}
    </div>
  )
}
