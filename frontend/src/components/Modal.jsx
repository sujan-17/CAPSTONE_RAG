import { useEffect } from 'react'
import './Modal.css'

const API_BASE = 'http://localhost:8000'

function Modal({ item, onClose }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [onClose])

  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [])

  const metadata = item.metadata || item
  const imageName = metadata.image_name || item.image_name
  const category = metadata.category || item.category || 'necklace'
  const imageUrl = imageName ? `${API_BASE}/static/${category}/${imageName}` : ''
  const description = metadata.short_description || item.description || 'No description available'

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          X
        </button>

        <div className="modal-body">
          <div className="modal-image-section">
            <img
              src={imageUrl}
              alt={description}
              className="modal-image"
            />
          </div>

          <div className="modal-details">
            <h2 className="modal-title">Jewelry Details</h2>

            <p className="modal-description">{description}</p>

            <div className="modal-attributes">
              <h3>Attributes</h3>

              <div className="attributes-grid">
                <div className="attribute-item">
                  <span className="attribute-label">Category</span>
                  <span className="attribute-value">{category}</span>
                </div>

                <div className="attribute-item">
                  <span className="attribute-label">Material</span>
                  <span className="attribute-value">
                    {metadata.material && metadata.material !== 'none'
                      ? metadata.material
                      : 'Not specified'}
                  </span>
                </div>

                <div className="attribute-item">
                  <span className="attribute-label">Stone Type</span>
                  <span className="attribute-value">
                    {metadata.stone_type && metadata.stone_type !== 'none'
                      ? metadata.stone_type
                      : 'None'}
                  </span>
                </div>

                <div className="attribute-item">
                  <span className="attribute-label">Stone Shape</span>
                  <span className="attribute-value">
                    {metadata.stone_shape && metadata.stone_shape !== 'none'
                      ? metadata.stone_shape
                      : 'Not specified'}
                  </span>
                </div>

                <div className="attribute-item">
                  <span className="attribute-label">Color</span>
                  <span className="attribute-value">
                    {metadata.color && metadata.color !== 'unknown'
                      ? metadata.color
                      : 'Not specified'}
                  </span>
                </div>
              </div>
            </div>

            {item.id && (
              <div className="modal-id">
                <span className="id-label">ID:</span>
                <span className="id-value">{item.id}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Modal
