// App.jsx
import { useState, useEffect } from 'react'
import SearchBox from './searchBox'
import MapComponent from './MapComponent'
import FirePreventionChatbot from './FirePreventionChatbot'
import './App.css'

export default function App() {
  const [demoOpen, setDemoOpen] = useState(false)
  const [hidden, setHidden] = useState(false)
  const [fires, setFires] = useState([])
  const [center, setCenter] = useState(null)
  const [isSearching, setIsSearching] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleSearchResults = (data) => {
    setFires(data.fires || [])
    setCenter(data.center || null)
    setIsSearching(false)
    if (data.fires && data.fires.length > 0) setTimeout(() => setShowResults(true), 100)
  }

  const handleSearchStart = () => {
    setIsSearching(true)
    setShowResults(false)
  }

  useEffect(() => {
    if (fires.length === 0) setShowResults(false)
  }, [fires.length])

  return (
    <>
      {/* Main App Container */}
      {!demoOpen && (
        <div className={`app ${hidden ? 'hidden' : ''}`}>
          <div className="app-controls">
          </div>

          <div className="app-header">
            <h1>We track fire near you</h1>
            <SearchBox onResults={handleSearchResults} onSearchStart={handleSearchStart} />
          </div>

          {isSearching && (
            <div className="search-loading">
              <div className="loading-pulse">
                <div className="pulse-dot"></div>
                <div className="pulse-dot"></div>
                <div className="pulse-dot"></div>
              </div>
              <p>Analyzing wildfire data...</p>
            </div>
          )}

          {fires.length > 0 && showResults ? (
            <MapComponent fires={fires} center={center} />
          ) : !isSearching ? (
            <div className="welcome-message">
              <p>Search for a location to see wildfires</p>
              <div className="search-hints">
                <span>Try: Vancouver, Prince George, or Kamloops</span>
              </div>
            </div>
          ) : null}
        </div>
      )}
      {/* Fire Prevention Chatbot */}
      <FirePreventionChatbot />
    </>
  )
}