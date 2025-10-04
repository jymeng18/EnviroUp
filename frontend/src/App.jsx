// frontend/src/App.jsx
import { useEffect, useState } from 'react';
import './App.css'
import SearchBox from './searchBox.jsx'

function App() {
  const [transactions, setTransactions] = useState([]);
  const [searchResults, setSearchResults] = useState(null)

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/transactions");
      const data = await response.json();
      setTransactions(data);
    } catch (error) {
      console.log('Error fetching transactions:', error);
    }
  }

  return (
    <div className="App">
      <h1 className="app-title">We track the wildfire near you</h1>

      <section className="search-section" style={{ marginBottom: 20 }}>
        <h3>Search for location</h3>
        <SearchBox onResults={data => setSearchResults(data)} />
        {searchResults && (
          <div style={{ marginTop: 12 }}>
            <h4>Search Results</h4>
            {Array.isArray(searchResults) ? (
              <ul>
                {searchResults.map(item => (
                  <li key={item.id || JSON.stringify(item)}>
                    {item.date ? `${item.date}: $${item.amount?.toFixed?.(2) ?? item.amount} - ${item.category ?? ''}` : JSON.stringify(item)}
                  </li>
                ))}
              </ul>
            ) : (
              <pre>{JSON.stringify(searchResults, null, 2)}</pre>
            )}
          </div>
        )}
      </section>


      <section className="info-section">
        <h3>Nearest wildfire</h3>
        
      </section>
    </div>
  );
}

export default App;
