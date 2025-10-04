import { useState } from 'react'

/**
 * SearchBox component
 * - Renders an input and a button
 * - Sends the query to the backend via POST to /api/search (JSON: { q })
 * - Shows loading and error states and returns the response to the caller
 */
export default function SearchBox({ onResults }) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const res = await fetch('/api/search', {
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
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <input
        type="search"
        placeholder="Search..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        style={{ padding: '8px 10px', flex: 1 }}
        aria-label="Search"
      />
      <button type="submit" disabled={loading || !query.trim()} style={{ padding: '8px 12px' }}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      {error && <div role="alert" style={{ color: 'var(--danger, #c00)', marginLeft: 8 }}>{error}</div>}
    </form>
  )
}
