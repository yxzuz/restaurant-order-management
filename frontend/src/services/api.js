import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    Accept: 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)

    // Handle token expiration (401 Unauthorized)
    if (error.response?.status === 401) {
      const token = localStorage.getItem('token')
      if (token) {
        // Token exists but is invalid/expired - clear it
        localStorage.removeItem('token')
        
        // Show user-friendly message
        console.warn('Your session has expired. Please log in again.')
        
        // Redirect to home page if not already there
        if (window.location.pathname !== '/') {
          window.location.href = '/'
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api
