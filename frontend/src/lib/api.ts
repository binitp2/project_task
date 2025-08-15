export const apiBaseUrl = 'http://127.0.0.1:8000'

export async function api(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token')
  
  // Debug: Log token status
  console.log('API: Making request to', endpoint, 'Token available:', !!token)
  
  const response = await fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Network error' }))
    console.error('API: Request failed:', endpoint, error)
    
    // If authentication failed, clear token and redirect to login
    if (response.status === 401) {
      console.log('API: Authentication failed, clearing token')
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    throw error
  }

  return response.json()
}

export function wsUrl() {
  const base = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
  const token = localStorage.getItem('token')
  const url = new URL(base)
  if (token) url.searchParams.set('token', token)
  return url.toString()
}


