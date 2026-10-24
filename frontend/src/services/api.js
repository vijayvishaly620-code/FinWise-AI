export const API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')

function getToken() {
  return localStorage.getItem('token')
}

async function request(endpoint, options = {}) {
  const token = getToken()
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Request failed')
  return data
}

export const auth = {
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  getProfile: () => request('/auth/profile'),
  updateProfile: (data) => request('/auth/profile', { method: 'PUT', body: JSON.stringify(data) }),
}

export const transactions = {
  getAll: (params = '') => request(`/transactions${params ? '?' + params : ''}`),
  create: (data) => request('/transactions', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/transactions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/transactions/${id}`, { method: 'DELETE' }),
}

export const budgets = {
  getAll: (month = '') => request(`/budgets${month ? '?month=' + month : ''}`),
  create: (data) => request('/budgets', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/budgets/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/budgets/${id}`, { method: 'DELETE' }),
}

export const savings = {
  getAll: () => request('/savings'),
  create: (data) => request('/savings', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/savings/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/savings/${id}`, { method: 'DELETE' }),
}

export const dashboard = {
  getSummary: (params = '') => request(`/dashboard/summary${params ? '?' + params : ''}`),
  getAnalytics: () => request('/dashboard/analytics'),
}

export const advisor = {
  analyze: () => request('/advisor/analyze', { method: 'POST' }),
  chat: (message) => request('/advisor/chat', { method: 'POST', body: JSON.stringify({ message }) }),
  predictExpenses: () => request('/advisor/predict-expenses', { method: 'POST' }),
  getHealth: () => request('/advisor/financial-health'),
}

export const reports = {
  getMonthly: (month, year) => request(`/reports/monthly?month=${month}&year=${year}`),
  getYearly: (year) => request(`/reports/yearly?year=${year}`),
  download: (start, end) => {
    const token = getToken()
    window.open(`${API_BASE}/reports/download?start_date=${start}&end_date=${end}&token=${token}`, '_blank')
  },
}

export const alerts = {
  getAll: (unread = false) => request(`/alerts${unread ? '?unread=true' : ''}`),
  markRead: (id) => request(`/alerts/${id}/read`, { method: 'PUT' }),
}

export const dataset = {
  getInfo: () => request('/dataset/info'),
}
