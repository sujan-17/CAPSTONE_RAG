import ResultCard from './ResultCard'
import './ResultsGrid.css'

function ResultsGrid({ results, loading, onItemClick }) {
  if (loading) {
    return (
      <div className="results-grid-loading">
        <div className="loading-container">
          <div className="loading-spinner-large"></div>
          <p>Searching for matching jewelry...</p>
        </div>
      </div>
    )
  }

  if (!results || results.length === 0) {
    return (
      <div className="results-grid-empty">
        <div className="empty-icon">0</div>
        <h3>No Results Found</h3>
        <p>Try adjusting your filters or search with different keywords</p>
      </div>
    )
  }

  return (
    <div className="results-grid">
      {results.map((item, index) => (
        <ResultCard
          key={item.id || index}
          item={item}
          onClick={() => onItemClick(item)}
          index={index}
        />
      ))}
    </div>
  )
}

export default ResultsGrid
