import { useState } from 'react'
import Enhance from './components/Enhance'
import Colorize from './components/Colorize'
import RemoveBg from './components/RemoveBg'
import './App.css'

function App() {
  const [tab, setTab] = useState('enhance')

  return (
    <div className="app">
      <div className="header">
        <div className="logo">Wash<span>Up</span> AI</div>
        <p className="subtitle">Enhance · Colorize · Remove Background</p>
      </div>

      <div className="tabs">
        <button onClick={() => setTab('enhance')} className={tab === 'enhance' ? 'active' : ''}>Enhance</button>
        <button onClick={() => setTab('colorize')} className={tab === 'colorize' ? 'active' : ''}>Colorize</button>
        <button onClick={() => setTab('removebg')} className={tab === 'removebg' ? 'active' : ''}>Remove BG</button>
      </div>

      <div className="content">
        {tab === 'enhance' && <Enhance />}
        {tab === 'colorize' && <Colorize />}
        {tab === 'removebg' && <RemoveBg />}
      </div>
    </div>
  )
}

export default App