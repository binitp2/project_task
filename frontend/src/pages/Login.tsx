import { useState } from 'react'
import { api } from '../lib/api'

export default function Login({ onLogin }: { onLogin: (token: string) => void }) {
  const [email, setEmail] = useState('alice@example.com')
  const [password, setPassword] = useState('Password@123')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!email.includes('@') || !password.length ) {
      setError('Enter a valid email and password')
      return
    }
    setLoading(true)
    try {
      const tokenRes = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password })})
      onLogin(tokenRes.access_token)
    } catch (err: any) {
      setError(err.detail || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  async function handleRegister(e: React.MouseEvent) {
    e.preventDefault()
    setError(null)
    if (!email.includes('@')) {
      setError('Enter a valid email.')
      return
    }
    if (!/(?=.*\d)(?=.*[^\w\s]).{8,}/.test(password)) {
      setError('Password must be 8+ chars, include a number and a special character.')
      return
    }
    setLoading(true)
    try {
      await api('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) })
      const tokenRes = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
      onLogin(tokenRes.access_token)
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login">
      <h2>Login</h2>
      <form className="form" onSubmit={handleSubmit} aria-label="Login form">
        <label className="field">
          <span>Email</span>
          <input aria-label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} autoComplete="off" />
        </label>
        <label className="field">
          <span>Password</span>
          <input aria-label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="off" />
        </label>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn" disabled={loading} type="submit">{loading ? 'Loading…' : 'Login'}</button>
          <button className="btn" disabled={loading} onClick={handleRegister}>Register</button>
        </div>
        {error && <div className="error" role="alert">{error}</div>}
      </form>
    </div>
  )
}


