import { useState, useCallback, useRef } from 'react'
import './ImageUpload.css'

function ImageUpload({ onSearch, loading }) {
  const [dragActive, setDragActive] = useState(false)
  const [preview, setPreview] = useState(null)
  const inputRef = useRef(null)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }, [])

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
    if (!validTypes.includes(file.type)) {
      alert('Please upload a valid image file (JPEG, PNG, or WebP)')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target.result)
    }
    reader.readAsDataURL(file)

    onSearch(file)
  }

  const handleClick = () => {
    inputRef.current?.click()
  }

  const clearPreview = (e) => {
    e.stopPropagation()
    setPreview(null)
    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }

  return (
    <div className="image-upload">
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${preview ? 'has-preview' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/jpg,image/webp"
          onChange={handleChange}
          className="file-input"
          disabled={loading}
        />

        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <button
              className="clear-preview"
              onClick={clearPreview}
              disabled={loading}
            >
              X
            </button>
            <div className="preview-overlay">
              <span>Click or drop to replace</span>
            </div>
          </div>
        ) : (
          <div className="upload-content">
            <div className="upload-icon">IMG</div>
            <p className="upload-text">
              <span className="upload-link">Upload an image</span> or drag and drop
            </p>
            <p className="upload-hint">PNG, JPG, WEBP up to 10MB</p>
          </div>
        )}
      </div>

      <p className="upload-description">
        Upload a jewelry image to find similar items in our collection
      </p>
    </div>
  )
}

export default ImageUpload
