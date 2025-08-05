import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import './index.css'

const saved = localStorage.getItem('theme') || 'light'
if (saved === 'dark') {
  document.documentElement.classList.add('dark')
}
console.log('Main.tsx is running');

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
