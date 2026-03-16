import { useState, useCallback } from 'react'
import axios from 'axios'
import SearchBox from './components/SearchBox'
import ImageUpload from './components/ImageUpload'
import ResultsGrid from './components/ResultsGrid'
import FilterPanel from './components/FilterPanel'
import Modal from './components/Modal'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [searchResults, setSearchResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedItem, setSelectedItem] = useState(null)
  const [filters, setFilters] = useState({
    category: [],
    material: [],
    stone_type: [],
    stone_shape: [],
    color: []
  })
  const [searchType, setSearchType] = useState('text')

  const handleTextSearch = async (query) => {
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setSearchType('text')

    try {
      const response = await axios.post(`${API_BASE}/search/text`, null, {
        params: { query }
      })
      setSearchResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Search failed')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleImageSearch = async (file) => {
    if (!file) return

    setLoading(true)
    setError(null)
    setSearchType('image')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE}/search/image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setSearchResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Image search failed')
      console.error('Image search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = useCallback((filterType, values) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: values
    }))
  }, [])

  const getFilteredResults = useCallback(() => {
    if (!searchResults?.results) return []

    return searchResults.results.filter(item => {
      const metadata = item.metadata || item
      return (
        (filters.category.length === 0 || filters.category.includes(metadata.category)) &&
        (filters.material.length === 0 || filters.material.includes(metadata.material)) &&
        (filters.stone_type.length === 0 || filters.stone_type.includes(metadata.stone_type)) &&
        (filters.stone_shape.length === 0 || filters.stone_shape.includes(metadata.stone_shape)) &&
        (filters.color.length === 0 || filters.color.includes(metadata.color))
      )
    })
  }, [searchResults, filters])

  const clearFilters = () => {
    setFilters({
      category: [],
      material: [],
      stone_type: [],
      stone_shape: [],
      color: []
    })
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-glow header-glow-left"></div>
        <div className="header-glow header-glow-right"></div>
        <div className="header-content">
          <div className="eyebrow">AI Powered Jewel Search</div>
          <div className="logo">
            <h1>Multimodal Jewel Search</h1>
          </div>
          <p className="tagline">
            Search for rings, necklaces, sketches, and image-based matches with AI-powered retrieval.
          </p>
          <div className="hero-pills">
            <span className="hero-pill">Text Retrieval</span>
            <span className="hero-pill">Image Search</span>
            <span className="hero-pill">Smart Filtering</span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="search-section">
          <div className="search-container">
            <div className="search-panel">
              <div className="panel-kicker">Describe the piece</div>
              <h2 className="panel-title">Search with language</h2>
              <p className="panel-copy">
                Type the jewelry style, material, or gemstone you want to explore.
              </p>
              <SearchBox onSearch={handleTextSearch} loading={loading} />
            </div>

            <div className="divider" aria-hidden="true">
              <span>OR</span>
            </div>

            <div className="search-panel">
              <div className="panel-kicker">Use visual search</div>
              <h2 className="panel-title">Upload an image</h2>
              <p className="panel-copy">
                Drop a jewelry image, reference photo, or sketch to find visually similar pieces.
              </p>
              <ImageUpload onSearch={handleImageSearch} loading={loading} />
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <span className="error-icon">!</span> {error}
          </div>
        )}

        {searchResults && (
          <div className="results-section">
            <div className="results-header">
              <div className="query-info">
                {searchResults.rewritten_query && (
                  <div className="rewritten-query">
                    <span className="label">Processed Query:</span>
                    <span className="value">"{searchResults.rewritten_query}"</span>
                  </div>
                )}

                <div className="meta-row">
                  {searchResults.category && (
                    <div className="category-badge">
                      <span className="category-icon">
                        {searchResults.category === 'necklace' ? 'N' : 'R'}
                      </span>
                      {searchResults.category}
                    </div>
                  )}

                  {searchType === 'image' && searchResults.query_type && (
                    <div className="query-type">
                      <span className="label">Query Type:</span>
                      <span className="value">{searchResults.query_type}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="results-count">
                {getFilteredResults().length} of {searchResults.results.length} results
              </div>
            </div>

            <div className="results-layout">
              <aside className="filter-sidebar">
                <FilterPanel
                  filters={filters}
                  onFilterChange={handleFilterChange}
                  onClear={clearFilters}
                  results={searchResults.results}
                />
              </aside>

              <div className="results-area">
                <ResultsGrid
                  results={getFilteredResults()}
                  loading={loading}
                  onItemClick={setSelectedItem}
                />
              </div>
            </div>
          </div>
        )}

        {!searchResults && !loading && (
          <div className="empty-state">
            <div className="empty-icon">O</div>
            <h2>Start Your Search</h2>
            <p>
              Search by natural language or upload a reference image to explore the collection in
              a more visual, modern way.
            </p>
          </div>
        )}
      </main>

      {selectedItem && (
        <Modal item={selectedItem} onClose={() => setSelectedItem(null)} />
      )}
    </div>
  )
}

export default App
