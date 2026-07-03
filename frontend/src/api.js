const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') ?? ''
  const isJson = contentType.includes('application/json')
  const payload = isJson ? await response.json() : await response.text()

  if (!response.ok) {
    const detail = isJson ? payload?.detail : null
    const message = detail?.message || (typeof payload === 'string' && payload) || `Request failed with status ${response.status}`
    throw new Error(message)
  }

  return payload
}

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  return parseResponse(response)
}

export async function apiDownload(path) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'include',
  })

  if (!response.ok) {
    const contentType = response.headers.get('content-type') ?? ''
    const payload = contentType.includes('application/json') ? await response.json() : await response.text()
    const detail = typeof payload === 'object' ? payload?.detail : null
    throw new Error(detail?.message || payload || `Download failed with status ${response.status}`)
  }

  return response
}
