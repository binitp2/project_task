import { useEffect, useState } from 'react'
import { api } from './api'

export function useMe() {
  const [email, setEmail] = useState<string | null>(null)
  useEffect(() => {
    api('/users/me').then((u) => setEmail(u.email)).catch(() => setEmail(null))
  }, [])
  return email
}


