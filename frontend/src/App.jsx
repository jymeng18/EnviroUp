// App.jsx
import { useState } from 'react'
import SearchBox from './searchBox'

function App() {
  const [fires, setFires] = useState([])

  const handleSearchResults = (data) => {
    setFires(data.fires || [])
  }

  return (
    <div className="app">
      <h1>BC Wildfire Tracker</h1>
      <SearchBox onResults={handleSearchResults} />
      
      {fires.length > 0 ? (
        <div className="fire-list">
          <h2>Found {fires.length} wildfires</h2>
          {fires.map((fire, idx) => (
            <div key={idx} className="fire-item">
              <h3>{fire.name}</h3>
              <p> {fire.latitude}, {fire.longitude}</p>
              <p> Severity: {fire.severity}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>Search for a location to see wildfires</p>
      )}
    </div>
  )
}

export default App