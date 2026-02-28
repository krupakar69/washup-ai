import { useState } from 'react'
import axios from 'axios'

export default function Enhance() {
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
      const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/enhance`, form, {
        responseType: 'blob',
        timeout: 300000
      })
      setResult(URL.createObjectURL(res.data))
    } catch (err) {
      setError('Enhancement failed. Make sure backend is running.')
    }
    setLoading(false)
  }

  return (
    <div className="feature-box">
      <h2>Photo Enhancement</h2>
      <div className="divider"></div>
      <p className="feature-desc">Upscale low quality images to high definition</p>

      <div className="upload-area" onClick={() => document.getElementById('enhance-input').click()}>
        <input id="enhance-input" type="file" accept="image/*" onChange={handleFile} />
        {preview
          ? <img src={preview} alt="input" style={{maxHeight:'200px', borderRadius:'10px'}} />
          : <>
              <div className="upload-icon">↑</div>
              <p className="upload-text">Click to upload an image</p>
            </>
        }
      </div>

      <button className="btn" onClick={handleSubmit} disabled={!file || loading}>
        {loading ? 'Enhancing... please wait' : 'Enhance Image'}
      </button>

      {error && <p className="status error">{error}</p>}

      {result && (
        <div className="preview-row">
          <div className="preview-box">
            <p className="preview-label">Original</p>
            <img src={preview} alt="original" />
          </div>
          <div className="preview-box">
            <p className="preview-label">Enhanced</p>
            <img src={result} alt="enhanced" />
            <a className="download-btn" href={result} download="enhanced.png">Download</a>
          </div>
        </div>
      )}
    </div>
  )
}