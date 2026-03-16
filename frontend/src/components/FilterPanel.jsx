import { useMemo } from 'react'
import './FilterPanel.css'

// Filter options based on metadata
const FILTER_OPTIONS = {
  category: ['necklace', 'ring'],
  material: ['gold', 'silver', 'rose gold', 'platinum', 'unknown'],
  stone_type: ['diamond', 'pearl', 'emerald', 'ruby', 'sapphire', 'none', 'unknown'],
  stone_shape: ['round', 'oval', 'heart', 'square', 'princess', 'none'],
  color: ['yellow', 'pink', 'white', 'blue', 'green', 'red', 'unknown']
}

function FilterPanel({ filters, onFilterChange, onClear, results }) {
  // Get available filter values from results
  const availableFilters = useMemo(() => {
    if (!results || results.length === 0) return {}
    
    const counts = {}
    Object.keys(FILTER_OPTIONS).forEach(key => {
      counts[key] = {}
      results.forEach(item => {
        const metadata = item.metadata || item
        const value = metadata[key]
        if (value && value !== 'none' && value !== 'unknown') {
          counts[key][value] = (counts[key][value] || 0) + 1
        }
      })
    })
    return counts
  }, [results])

  const handleFilterToggle = (filterType, value) => {
    const current = filters[filterType]
    const newValues = current.includes(value)
      ? current.filter(v => v !== value)
      : [...current, value]
    onFilterChange(filterType, newValues)
  }

  const hasActiveFilters = Object.values(filters).some(arr => arr.length > 0)

  return (
    <div className="filter-panel">
      <div className="filter-header">
        <h3>Filters</h3>
        {hasActiveFilters && (
          <button className="clear-filters" onClick={onClear}>
            Clear All
          </button>
        )}
      </div>

      <div className="filter-sections">
        {/* Category Filter */}
        <div className="filter-section">
          <h4>Category</h4>
          <div className="filter-options">
            {FILTER_OPTIONS.category.map(value => (
              <label key={value} className="filter-option">
                <input
                  type="checkbox"
                  checked={filters.category.includes(value)}
                  onChange={() => handleFilterToggle('category', value)}
                />
                <span className="option-label">{value}</span>
                {availableFilters.category?.[value] && (
                  <span className="option-count">{availableFilters.category[value]}</span>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Material Filter */}
        <div className="filter-section">
          <h4>Material</h4>
          <div className="filter-options">
            {FILTER_OPTIONS.material.map(value => (
              <label key={value} className="filter-option">
                <input
                  type="checkbox"
                  checked={filters.material.includes(value)}
                  onChange={() => handleFilterToggle('material', value)}
                />
                <span className="option-label">{value}</span>
                {availableFilters.material?.[value] && (
                  <span className="option-count">{availableFilters.material[value]}</span>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Stone Type Filter */}
        <div className="filter-section">
          <h4>Stone Type</h4>
          <div className="filter-options">
            {FILTER_OPTIONS.stone_type.map(value => (
              <label key={value} className="filter-option">
                <input
                  type="checkbox"
                  checked={filters.stone_type.includes(value)}
                  onChange={() => handleFilterToggle('stone_type', value)}
                />
                <span className="option-label">{value}</span>
                {availableFilters.stone_type?.[value] && (
                  <span className="option-count">{availableFilters.stone_type[value]}</span>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Stone Shape Filter */}
        <div className="filter-section">
          <h4>Stone Shape</h4>
          <div className="filter-options">
            {FILTER_OPTIONS.stone_shape.map(value => (
              <label key={value} className="filter-option">
                <input
                  type="checkbox"
                  checked={filters.stone_shape.includes(value)}
                  onChange={() => handleFilterToggle('stone_shape', value)}
                />
                <span className="option-label">{value}</span>
                {availableFilters.stone_shape?.[value] && (
                  <span className="option-count">{availableFilters.stone_shape[value]}</span>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Color Filter */}
        <div className="filter-section">
          <h4>Color</h4>
          <div className="filter-options">
            {FILTER_OPTIONS.color.map(value => (
              <label key={value} className="filter-option">
                <input
                  type="checkbox"
                  checked={filters.color.includes(value)}
                  onChange={() => handleFilterToggle('color', value)}
                />
                <span className="option-label">{value}</span>
                {availableFilters.color?.[value] && (
                  <span className="option-count">{availableFilters.color[value]}</span>
                )}
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FilterPanel
