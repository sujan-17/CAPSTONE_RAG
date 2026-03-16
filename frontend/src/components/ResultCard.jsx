import { useState } from 'react'
import './ResultCard.css'

const API_BASE = 'http://localhost:8000'

function ResultCard({ item, onClick, index }) {
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)

  const metadata = item.metadata || item
  const imageName = metadata.image_name || item.image_name
  const category = metadata.category || item.category || 'necklace'
  const imageUrl = imageName ? `${API_BASE}/static/${category}/${imageName}` : ''
  const description = metadata.short_description || item.description || 'No description available'

  const handleImageLoad = () => {
    setImageLoaded(true)
  }

  const handleImageError = () => {
    setImageError(true)
    setImageLoaded(true)
  }

  return (
    <div
      className={`result-card ${imageLoaded ? 'loaded' : ''}`}
      onClick={onClick}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="card-image-container">
        {!imageError ? (
          <img
            src={imageUrl}
            alt={description}
            className={`card-image ${imageLoaded ? 'loaded' : ''}`}
            onLoad={handleImageLoad}
            onError={handleImageError}
          />
        ) : (
          <div className="card-image-placeholder">
            <span>IMG</span>
          </div>
        )}
      </div>

      <div className="card-content">
        <p className="card-description">{description}</p>
        <div className="card-tags">
          {metadata.material && metadata.material !== 'none' && (
            <span className="tag material">{metadata.material}</span>
          )}
          {metadata.stone_type && metadata.stone_type !== 'none' && (
            <span className="tag stone">{metadata.stone_type}</span>
          )}
        </div>
      </div>
    </div>
  )
}

export default ResultCard
