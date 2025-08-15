import { useEffect, useMemo, useState } from 'react'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Inbox from './pages/Inbox'
import Chat from './pages/Chat'
import BotChat from './pages/BotChat'
import ActivityPage from './pages/Activity'

function App() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const navigate = useNavigate()

  useEffect(() => {
    if (!token && location.pathname !== '/login') {
      navigate('/login')
    }
  }, [token])

  const onLogin = (t: string) => {
    localStorage.setItem('token', t)
    setToken(t)
    navigate('/')
  }

  const onLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    navigate('/login')
  }

  return (
    <div className="app" role="application">
      <nav className="topbar" aria-label="Main">
        <Link to="/">Inbox</Link>
        <Link to="/bot">Bot Chat</Link>
        <Link to="/activity">Activity</Link>
        {token && <button onClick={onLogout} aria-label="Logout">Logout</button>}
      </nav>
      <Routes>
        <Route path="/login" element={<Login onLogin={onLogin} />} />
        <Route path="/" element={<Inbox />} />
        <Route path="/chat/:peer" element={<Chat />} />
        <Route path="/bot" element={<BotChat />} />
        <Route path="/activity" element={<ActivityPage />} />
      </Routes>
    </div>
  )
}

export default App


