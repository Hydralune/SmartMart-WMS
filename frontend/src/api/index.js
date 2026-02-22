import http from './http'

export const authApi = {
  login: (data) => http.post('/auth/login', data),
}

export const productsApi = {
  list: (params) => http.get('/products', { params }),
  create: (data) => http.post('/products', data),
  update: (id, data) => http.put(`/products/${id}`, data),
  remove: (id) => http.delete(`/products/${id}`),
}

export const inventoryApi = {
  list: (params) => http.get('/inventory', { params }),
}

export const inboundApi = {
  list: () => http.get('/inbound'),
  create: (data) => http.post('/inbound', data),
}

export const outboundApi = {
  list: () => http.get('/outbound'),
  create: (data) => http.post('/outbound', data),
}

export const stocktakeApi = {
  list: () => http.get('/stocktake'),
  create: (data) => http.post('/stocktake', data),
  approve: (id) => http.put(`/stocktake/${id}/approve`),
}

export const suppliersApi = {
  list: () => http.get('/suppliers'),
  create: (data) => http.post('/suppliers', data),
  update: (id, data) => http.put(`/suppliers/${id}`, data),
  remove: (id) => http.delete(`/suppliers/${id}`),
}

export const statsApi = {
  inventory: () => http.get('/stats/inventory'),
  trend: () => http.get('/stats/trend'),
}

export const logsApi = {
  list: () => http.get('/logs'),
  exportBackup: () => http.get('/logs/backup/export', { responseType: 'blob' }),
}
