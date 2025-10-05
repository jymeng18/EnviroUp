// App.jsx
import { useState, useEffect } from 'react'
import SearchBox from './searchBox'
import MapComponent from './MapComponent'


function App() {
  const [fires, setFires] = useState([])
  const [center, setCenter] = useState(null)
  const [isSearching, setIsSearching] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleSearchResults = (data) => {
    setFires(data.fires || [])
    setCenter(data.center || null)
    setIsSearching(false)
    
    // Trigger animation for results
    if (data.fires && data.fires.length > 0) {
      setTimeout(() => setShowResults(true), 100)
    }
  }

  const handleSearchStart = () => {
    setIsSearching(true)
    setShowResults(false)
  }

  // Reset search state when fires are cleared
  useEffect(() => {
    if (fires.length === 0) {
      setShowResults(false)
    }
  }, [fires.length])

  return (
    <div className="app">
      <div className="app-header">
        <h1>Hi we track fire near you</h1>
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
            <span>Try: Vancouver, British Columbia, Kamloops</span>
          </div>
        </div>
      ) : null}
    </div>
  )
}

export default App