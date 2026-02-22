import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import router from '@/router'

const http = axios.create({ baseURL: '/api/v1', timeout: 15000 })

http.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  res => res.data,
  err => {
    const status = err.response?.status
    if (status === 401 || status === 422) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
    return Promise.reject(err)
  }
)

export default http
