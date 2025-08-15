import Chat from './Chat'

export default function BotChat() {
  // Reuse Chat route with special peer set via router path '/bot' → component sets window.location to /chat/BOT
  // But simpler: inline a minimal proxy that renders Chat with a spoofed param is harder. We'll redirect.
  window.location.replace(`/chat/${encodeURIComponent('whatsease_bot')}`)
  return null
}


