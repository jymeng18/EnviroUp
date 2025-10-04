// frontend/src/App.jsx
import { useEffect, useState } from 'react';
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
      <h1>Finance Tracker Dashboard</h1>

      <section style={{ marginBottom: 20 }}>
        <h3>Search Transactions</h3>
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

      <h3>Recent Transactions</h3>
      <ul>
        {transactions.map(t => (
          <li key={t.id}>
            {t.date}: ${t.amount.toFixed(2)} - {t.category}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
