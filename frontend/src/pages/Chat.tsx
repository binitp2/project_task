import React, { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../lib/api'
import { getSocket } from '../lib/socket'
import { useMe } from '../lib/useMe'

type Msg = {
  id: string
  sender: string
  recipient: string
  content: string
  timestamp: string
  status: 'Sent' | 'Delivered' | 'Read'
  is_bot_response: boolean
}

export default function Chat() {
  const { peer = '' } = useParams()
  const [messages, setMessages] = useState<Msg[]>([])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(true)
  const sioRef = useRef<ReturnType<typeof getSocket> | null>(null)
  const me = useMe()

  useEffect(() => {
    let isMounted = true
    setLoading(true)
    
    // Debug: Check authentication status
    const token = localStorage.getItem('token')
    console.log('Chat: Token available:', !!token)
    console.log('Chat: Current user:', me)
    
    api(`/messages?peer=${encodeURIComponent(peer)}`).then((res) => {
      if (isMounted) {
        setMessages(res)
        // Mark unread messages as read when opening the chat
        if (me) {
          const s = sioRef.current || getSocket()
          res.filter((m: Msg) => m.recipient === me && m.status !== 'Read').forEach((m: Msg) => {
            s.emit('mark_read', { message_id: m.id })
          })
        }
      }
    }).catch((error) => {
      console.error('Chat: Failed to fetch messages:', error)
      if (isMounted) setMessages([])
    }).finally(() => setLoading(false))
    return () => { isMounted = false }
  }, [peer, me])

  useEffect(() => {
    const s = getSocket()
    sioRef.current = s
    const onMessage = (incoming: Msg) => {
      setMessages(prev => [...prev, incoming])
      if (me && incoming.recipient === me) {
        // report read via socket for immediate feedback
        s.emit('mark_read', { message_id: incoming.id })
      }
      // Notify inbox to increment unread when I am not the recipient (i.e., for other peers viewing their list)
      if (me && incoming.recipient === me) {
        // My unread handled by mark_read above (zero). For other tabs/users the server handles.
      }
    }
    const onStatus = (p: { message_id: string, status: 'Delivered' | 'Read' }) => {
      setMessages(prev => prev.map(m => m.id === p.message_id ? { ...m, status: p.status } as Msg : m))
    }
    s.on('message', onMessage)
    s.on('status', onStatus)
    return () => { s.off('message', onMessage); s.off('status', onStatus) }
  }, [me])

  async function send()
  {
    if (!text.trim()) return
    
    // Debug: Check authentication before sending
    const token = localStorage.getItem('token')
    console.log('Chat: Sending message, token available:', !!token)
    console.log('Chat: Current user:', me)
    
    const s = sioRef.current || getSocket()
    try {
      if (!s.connected) {
        await new Promise<void>((resolve, reject) => {
          s.connect()
          const to = setTimeout(() => reject(new Error('socket-timeout')), 1500)
          s.once('connect', () => { clearTimeout(to); resolve() })
          s.once('connect_error', (e: any) => { clearTimeout(to); reject(e) })
        })
      }
      s.emit('send_message', { recipient: peer, content: text })
    } catch {
      // Fallback to REST if socket not available
      try {
        console.log('Chat: Using REST fallback for message sending')
        const res = await api('/messages', { method: 'POST', body: JSON.stringify({ recipient: peer, content: text }) })
        setMessages(prev => [...prev, res])
      } catch (e) {
        console.error('Chat: REST send failed:', e)
      }
    } finally {
      setText('')
    }
  }

  return (
    <div className="content">
      <div className="chat-header">Chat with {peer}</div>
      <div className="messages" aria-live="polite">
      {loading ? 'Loading…' : messages.map((m: Msg) => {
          const isMine = me ? m.sender === me : false
          return (
          <div key={m.id} className={`bubble ${isMine ? 'me' : 'other'}`} aria-label={`${m.status}`}>
            <div>{m.content}</div>
            <small>{new Date(m.timestamp).toLocaleTimeString()} — {m.status}</small>
          </div>
        )})}
      </div>
      <div className="composer">
        <input aria-label="Message" value={text} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setText(e.target.value)} onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => { if (e.key === 'Enter') send() }} />
        <button onClick={send} aria-label="Send">Send</button>
      </div>
    </div>
  )
}


