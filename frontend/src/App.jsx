// frontend/src/App.jsx
import { useEffect, useState } from 'react';

function App() {
  const [transactions, setTransactions] = useState([]);

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
