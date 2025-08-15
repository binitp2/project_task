import { useEffect, useState } from 'react'
import { api } from '../lib/api'

type Activity = { user_email: string, action: string, details: string, timestamp: string }

export default function ActivityPage() {
  const [items, setItems] = useState<Activity[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchActivities = () => {
      console.log('Activity: Fetching activities...')
      api('/activity').then((activities) => {
        console.log('Activity: Activities received:', activities)
        setItems(activities)
      }).catch((e) => {
        console.error('Activity: Failed to fetch activities:', e)
        setError(String(e))
      })
    }

    // Fetch immediately
    fetchActivities()
    
    // Refresh every 5 seconds to show new activities
    const interval = setInterval(fetchActivities, 5000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ padding: 16 }}>
      <h2>Recent Activity</h2>
      {error && <div role="alert" style={{ color: 'crimson' }}>{error}</div>}
      <ul className="list">
        {items.map((a, i) => (
          <li key={i} className="list-item">
            <div><strong>{a.action}</strong></div>
            <div>{a.details}</div>
            <small>{new Date(a.timestamp).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  )
}


