import './App.css'

import { useEffect, useState } from 'react'

// In dev (Vite on :5173) talk to FastAPI on :8000.
// When served by FastAPI itself, relative `/api/v1` works.
const API_BASE =
  typeof window !== 'undefined' && window.location.port === '5173'
    ? 'http://localhost:8000/api/v1'
    : '/api/v1'

function getStoredToken() {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('stockpulse_token')
}

function storeToken(token) {
  if (typeof window === 'undefined') return
  if (token) {
    localStorage.setItem('stockpulse_token', token)
  } else {
    localStorage.removeItem('stockpulse_token')
  }
}

function App() {
  const [activeTab, setActiveTab] = useState('stocks')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [stocks, setStocks] = useState([])
  const [selectedSymbol, setSelectedSymbol] = useState('')
  const [history, setHistory] = useState([])

  const [wishlist, setWishlist] = useState([])
  const [orders, setOrders] = useState([])

  const [token, setToken] = useState(getStoredToken())
  const [authError, setAuthError] = useState('')

  async function fetchJson(url, options = {}) {
    setError('')
    setAuthError('')
    setLoading(true)
    try {
      const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      }
      if (token) {
        headers.Authorization = `Bearer ${token}`
      }

      const res = await fetch(url, {
        headers,
        ...options,
      })
      if (!res.ok) {
        const text = await res.text()
        if (res.status === 401) {
          setAuthError('You are not logged in. Please login to access this data.')
        }
        throw new Error(text || `Request failed with ${res.status}`)
      }
      if (res.status === 204) return null
      return await res.json()
    } catch (e) {
      setError(e.message || 'Something went wrong')
      return null
    } finally {
      setLoading(false)
    }
  }

  // Load base data
  useEffect(() => {
    loadStocks()
    loadWishlist()
    loadOrders()
  }, [])

  async function loadStocks() {
    const data = await fetchJson(`${API_BASE}/stocks`)
    if (data) setStocks(data)
  }

  async function loadHistory(symbol) {
    setSelectedSymbol(symbol)
    const data = await fetchJson(`${API_BASE}/stocks/history/${symbol}?days=30`)
    if (data) setHistory(data)
  }

  async function loadWishlist() {
    const data = await fetchJson(`${API_BASE}/wishlist`)
    if (data) setWishlist(data)
  }

  async function addToWishlist(symbol) {
    const body = JSON.stringify({ symbol })
    const data = await fetchJson(`${API_BASE}/wishlist`, {
      method: 'POST',
      body,
    })
    if (data) {
      await loadWishlist()
    }
  }

  async function removeFromWishlist(symbol) {
    const ok = await fetchJson(`${API_BASE}/wishlist/${symbol}`, {
      method: 'DELETE',
    })
    if (ok !== null) {
      await loadWishlist()
    }
  }

  async function loadOrders() {
    const data = await fetchJson(`${API_BASE}/orders`)
    if (data) setOrders(data)
  }

  function formatCurrency(v, currency = 'INR') {
    if (v == null) return '-'
    try {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency,
        maximumFractionDigits: 2,
      }).format(v)
    } catch {
      return v
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>StockPulse Dashboard</h1>
          <p className="subtitle">
            Simple UI on top of your FastAPI backend (`/api/v1`)
          </p>
        </div>
        <AuthPanel
          token={token}
          setToken={(t) => {
            setToken(t)
            storeToken(t)
          }}
          setError={setError}
          setAuthError={setAuthError}
        />
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'stocks' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('stocks')}
        >
          Stocks
        </button>
        <button
          className={activeTab === 'wishlist' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('wishlist')}
        >
          Wishlist
        </button>
        <button
          className={activeTab === 'orders' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('orders')}
        >
          Orders
        </button>
      </nav>

      {loading && <div className="banner info">Loading...</div>}
      {authError && <div className="banner warning">{authError}</div>}
      {error && <div className="banner error">{error}</div>}

      <main className="content">
        {activeTab === 'stocks' && (
          <section>
            <div className="section-header">
              <h2>Stocks</h2>
              <button className="secondary" onClick={loadStocks}>
                Refresh
              </button>
            </div>
            <p className="helper">
              Data from <code>/api/v1/stocks</code> and{' '}
              <code>/api/v1/stocks/history/&lt;symbol&gt;</code>.
            </p>

            <div className="grid">
              <div className="card">
                <h3>All Stocks</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Symbol</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Change</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      {stocks.map((s) => (
                        <tr key={s.id || s.symbol}>
                          <td>{s.symbol}</td>
                          <td>{s.name}</td>
                          <td>{formatCurrency(s.current_price, s.currency || 'INR')}</td>
                          <td
                            className={
                              s.change_percent > 0
                                ? 'positive'
                                : s.change_percent < 0
                                ? 'negative'
                                : ''
                            }
                          >
                            {s.change_percent?.toFixed
                              ? `${s.change_percent.toFixed(2)}%`
                              : s.change_percent}
                          </td>
                          <td className="actions">
                            <button onClick={() => loadHistory(s.symbol)}>
                              View 30d
                            </button>
                            <button
                              className="secondary"
                              onClick={() => addToWishlist(s.symbol)}
                            >
                              + Wishlist
                            </button>
                          </td>
                        </tr>
                      ))}
                      {stocks.length === 0 && (
                        <tr>
                          <td colSpan="5">No stocks found.</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="card">
                <h3>
                  Price History{' '}
                  {selectedSymbol ? `(${selectedSymbol} - 30 days)` : ''}
                </h3>
                {selectedSymbol ? (
                  history.length ? (
                    <HistoryChart data={history} />
                  ) : (
                    <p>No history data.</p>
                  )
                ) : (
                  <p>Select a stock to view history.</p>
                )}
              </div>
            </div>
          </section>
        )}

        {activeTab === 'wishlist' && (
          <section>
            <div className="section-header">
              <h2>Wishlist</h2>
              <button className="secondary" onClick={loadWishlist}>
                Refresh
              </button>
            </div>
            <p className="helper">
              Uses <code>/api/v1/wishlist</code> (GET, POST, DELETE).
            </p>
            <div className="card">
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Added At</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {wishlist.map((w) => (
                      <tr key={w.id || w.symbol}>
                        <td>{w.symbol}</td>
                        <td>
                          {w.created_at
                            ? new Date(w.created_at).toLocaleString()
                            : '-'}
                        </td>
                        <td className="actions">
                          <button
                            className="secondary"
                            onClick={() => removeFromWishlist(w.symbol)}
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                    {wishlist.length === 0 && (
                      <tr>
                        <td colSpan="3">Your wishlist is empty.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        )}

        {activeTab === 'orders' && (
          <section>
            <div className="section-header">
              <h2>Orders</h2>
              <button className="secondary" onClick={loadOrders}>
                Refresh
              </button>
            </div>
            <p className="helper">
              Data from <code>/api/v1/orders</code>.
            </p>
            <div className="card">
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Qty</th>
                      <th>Price/Unit</th>
                      <th>Total</th>
                      <th>Status</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map((o) => (
                      <tr key={o.id}>
                        <td>{o.symbol}</td>
                        <td>{o.quantity}</td>
                        <td>
                          {formatCurrency(o.price_per_unit, o.currency || 'INR')}
                        </td>
                        <td>
                          {formatCurrency(
                            (o.price_per_unit || 0) * (o.quantity || 0),
                            o.currency || 'INR',
                          )}
                        </td>
                        <td>{o.status || '-'}</td>
                        <td>
                          {o.created_at
                            ? new Date(o.created_at).toLocaleString()
                            : '-'}
                        </td>
                      </tr>
                    ))}
                    {orders.length === 0 && (
                      <tr>
                        <td colSpan="6">No orders yet.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

function HistoryChart({ data }) {
  if (!data.length) return null

  const min = Math.min(...data.map((d) => d.close))
  const max = Math.max(...data.map((d) => d.close))
  const range = max - min || 1

  return (
    <div className="history-chart">
      <div className="chart-header">
        <span>{data[0].date}</span>
        <span>{data[data.length - 1].date}</span>
      </div>
      <div className="chart-bars">
        {data.map((point) => {
          const h = ((point.close - min) / range) * 100
          return (
            <div
              key={point.date}
              className="bar"
              style={{ height: `${h}%` }}
              title={`${point.date} - ${point.close}`}
            />
          )
        })}
      </div>
      <div className="chart-footer">
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  )
}

function AuthPanel({ token, setToken, setError, setAuthError }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)

  const isLoggedIn = !!token

  async function handleLogin(e) {
    e.preventDefault()
    setError('')
    setAuthError('')
    setBusy(true)
    try {
      const body = new URLSearchParams()
      body.append('username', email)
      body.append('password', password)

      const res = await fetch(
        API_BASE.replace('/api/v1', '/api/v1/auth/login'),
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body,
        },
      )

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `Login failed with ${res.status}`)
      }

      const data = await res.json()
      if (data?.access_token) {
        setToken(data.access_token)
      } else {
        throw new Error('Login response did not contain access_token')
      }
    } catch (err) {
      setAuthError(
        'Login failed. Please check your email/password and verification status.',
      )
      console.error(err)
    } finally {
      setBusy(false)
    }
  }

  function handleLogout() {
    setToken(null)
    setEmail('')
    setPassword('')
  }

  return (
    <div className="auth-panel">
      {isLoggedIn ? (
        <>
          <span className="auth-status">Logged in</span>
          <button className="secondary small" onClick={handleLogout}>
            Logout
          </button>
        </>
      ) : (
        <form className="auth-form" onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button className="small" type="submit" disabled={busy}>
            {busy ? 'Logging in...' : 'Login'}
          </button>
        </form>
      )}
    </div>
  )
}

export default App
