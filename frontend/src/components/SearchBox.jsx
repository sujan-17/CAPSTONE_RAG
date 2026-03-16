import { useState } from 'react'
import './SearchBox.css'

function SearchBox({ onSearch, loading }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      if (query.trim()) {
        onSearch(query)
      }
    }
  }

  return (
    <div className="search-box">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <span className="search-icon">Q</span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search for jewelry... (e.g., 'gold diamond necklace')"
            className="search-input"
            disabled={loading}
          />
          {query && (
            <button
              type="button"
              className="clear-button"
              onClick={() => setQuery('')}
            >
              X
            </button>
          )}
        </div>

        <button
          type="submit"
          className="search-button"
          disabled={loading || !query.trim()}
        >
          {loading ? (
            <span className="loading-spinner"></span>
          ) : (
            'Search'
          )}
        </button>
      </form>

      <p className="search-hint">
        Try: "gold necklace with diamonds", "pearl ring", "rose gold bracelet"
      </p>
    </div>
  )
}

export default SearchBox
