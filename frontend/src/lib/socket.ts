import { io, Socket } from 'socket.io-client'

const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

let socket: Socket | null = null

export function getSocket(): Socket {
  if (socket) return socket
  const token = localStorage.getItem('token')
  socket = io(BASE, {
    path: '/socket.io',
    auth: token ? { token } : undefined,
    transports: ['websocket'],
    withCredentials: false,
    query: token ? { token } : {},
  })
  return socket
}


