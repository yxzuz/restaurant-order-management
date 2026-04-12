import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
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

    if (error?.response?.status === 401 || error?.response?.status === 403) {
      localStorage.removeItem('token')
      localStorage.removeItem('user_role')

      if (window.location.pathname !== '/') {
        window.location.href = '/'
      }
    }

    return Promise.reject(error)
  }
)

export default api
