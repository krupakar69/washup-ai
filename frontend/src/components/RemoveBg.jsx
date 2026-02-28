import { useState } from 'react'
import axios from 'axios'

export default function RemoveBg() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFile = (e) => {
    const f = e.target.files[0]
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
    setError('')
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/removebg`, form, {
        responseType: 'blob',
        timeout: 300000
      })
      setResult(URL.createObjectURL(res.data))
    } catch (err) {
      setError('Background removal failed. Make sure backend is running.')
    }
    setLoading(false)
  }

  return (
    <div className="feature-box">
      <h2>Remove Background</h2>
      <div className="divider"></div>
      <p className="feature-desc">Instantly remove image backgrounds with AI precision</p>

      <div className="upload-area" onClick={() => document.getElementById('removebg-input').click()}>
        <input id="removebg-input" type="file" accept="image/*" onChange={handleFile} />
        {preview
          ? <img src={preview} alt="input" style={{maxHeight:'200px', borderRadius:'10px'}} />
          : <>
              <div className="upload-icon">↑</div>
              <p className="upload-text">Click to upload an image</p>
            </>
        }
      </div>

      <button className="btn" onClick={handleSubmit} disabled={!file || loading}>
        {loading ? 'Processing... please wait' : 'Remove Background'}
      </button>

      {error && <p className="status error">{error}</p>}

      {result && (
        <div className="preview-row">
          <div className="preview-box">
            <p className="preview-label">Original</p>
            <img src={preview} alt="original" />
          </div>
          <div className="preview-box">
            <p className="preview-label">Background Removed</p>
            <img src={result} alt="no bg" style={{background:'repeating-conic-gradient(#e8f4ff 0% 25%, #f8fcff 0% 50%) 0 0 / 20px 20px', borderRadius:'12px'}} />
            <a className="download-btn" href={result} download="nobg.png">Download</a>
          </div>
        </div>
      )}
    </div>
  )
}