import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api'
import { getSocket } from '../lib/socket'

type User = { email: string, unread: number }

export default function Inbox() {
  const [users, setUsers] = useState<User[]>([])
  const [q, setQ] = useState('')

  useEffect(() => {
    console.log('Inbox: Fetching users...')
    const fetchUsers = () => {
      api('/users').then((users) => {
        console.log('Inbox: Users received:', users)
        setUsers(users)
      }).catch((error) => {
        console.error('Inbox: Failed to fetch users:', error)
        setUsers([])
      })
    }

    fetchUsers()
    const interval = setInterval(fetchUsers, 3000)

    // Realtime unread updates
    const s = getSocket()
    const onUnread = (p: { peer: string, unread: number }) => {
      setUsers(prev => prev.map(u => u.email === p.peer ? { ...u, unread: p.unread } : u))
    }
    s.on('unread', onUnread)

    return () => { clearInterval(interval); s.off('unread', onUnread) }
  }, [])

  const filtered = useMemo(() => users.filter(u => u.email.toLowerCase().includes(q.toLowerCase())), [users, q])

  return (
    <div className="layout">
      <aside className="sidebar" aria-label="Chats">
        <div className="searchbar">
          <input aria-label="Search users" placeholder="Search users" value={q} onChange={e => setQ(e.target.value)} />
        </div>
        <ul className="list" role="listbox">
          {filtered.map(u => (
            <li key={u.email} className="list-item" tabIndex={0}>
              <Link to={`/chat/${encodeURIComponent(u.email)}`}>{u.email}</Link>
              {u.unread > 0 && <span className="badge" aria-label={`${u.unread} unread messages`}>{u.unread}</span>}
            </li>
          ))}
          <li className="list-item"><Link to="/bot">Chat with Bot</Link></li>
        </ul>
      </aside>
      <main className="content" aria-live="polite">
        <div className="chat-header">Select a chat</div>
      </main>
    </div>
  )
}


