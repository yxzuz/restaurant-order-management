import api from '@/services/api'

function ownerAuthConfig() {
  const token = localStorage.getItem('token')
  return token
    ? { headers: { Authorization: `Bearer ${token}` } }
    : {}
}

export function normalizeMenuItem(item) {
  return {
    ...item,
    price: Number(item.price ?? 0),
    description: item.description ?? '',
    is_available: Boolean(item.is_available),
  }
}

export function getOrderItemSubtotal(item) {
  const explicitSubtotal = Number(item?.subtotal)
  if (!Number.isNaN(explicitSubtotal) && explicitSubtotal > 0) {
    return explicitSubtotal
  }

  return Number(item?.quantity ?? 0) * Number(item?.unit_price ?? 0)
}

export function getOrderTotal(order) {
  const explicitTotal = Number(order?.total_amount)
  if (!Number.isNaN(explicitTotal) && explicitTotal > 0) {
    return explicitTotal
  }

  return (order?.items || []).reduce((sum, item) => sum + getOrderItemSubtotal(item), 0)
}

export function normalizeOrder(order) {
  const items = (order.items || []).map((item) => ({
    ...item,
    unit_price: Number(item.unit_price ?? 0),
    subtotal: getOrderItemSubtotal(item),
  }))

  return {
    ...order,
    items,
    table_number: order.table_number ?? order.table?.number ?? null,
    total_amount: getOrderTotal({ ...order, items }),
  }
}

export async function fetchOwnerOrders() {
  const orders = await api.get('/orders/')
  return Array.isArray(orders) ? orders.map(normalizeOrder) : []
}

export async function fetchOwnerMenuItems() {
  const menuItems = await api.get('/menus/')
  return Array.isArray(menuItems) ? menuItems.map(normalizeMenuItem) : []
}

export async function updateOrderStatus(orderId, status) {
  const order = await api.patch(`/orders/${orderId}/status`, { status }, ownerAuthConfig())
  return normalizeOrder(order)
}

export async function updateOrderPayment(orderId, paymentStatus) {
  const order = await api.patch(`/orders/${orderId}/payment`, { payment_status: paymentStatus }, ownerAuthConfig())
  return normalizeOrder(order)
}

export async function updateOrderItemStatus(orderId, itemId, status) {
  const order = await api.patch(`/orders/${orderId}/items/${itemId}/status`, { status }, ownerAuthConfig())
  return normalizeOrder(order)
}

export async function cancelOrderItem(orderId, itemId) {
  const order = await api.delete(`/orders/${orderId}/items/${itemId}`, ownerAuthConfig())
  return normalizeOrder(order)
}

export async function deleteMenuItem(itemId) {
  await api.delete(`/menus/${itemId}`, ownerAuthConfig())
}

export async function createMenuItem(payload) {
  const formData = buildMenuItemFormData(payload)
  const item = await api.post('/menus/', formData, ownerAuthConfig())

  return normalizeMenuItem(item)
}

export async function updateMenuItem(itemId, payload) {
  const formData = buildMenuItemFormData(payload)
  const item = await api.patch(`/menus/${itemId}`, formData, ownerAuthConfig())

  return normalizeMenuItem(item)
}

export async function fetchUsers() {
  const users = await api.get('/auth/debug/users')
  return Array.isArray(users) ? users : []
}

export async function fetchTableAccessLinks() {
  const tables = await api.get('/tables/access-links', ownerAuthConfig())
  return Array.isArray(tables)
    ? tables.map((table) => ({
        ...table,
        number: Number(table.number ?? 0),
      }))
    : []
}

export async function createTable(number) {
  return api.post('/tables/', { number }, ownerAuthConfig())
}

export async function deleteTable(tableNumber) {
  await api.delete(`/tables/${tableNumber}`, ownerAuthConfig())
}

export async function createStaff(payload) {
  return api.post('/auth/staff', payload, ownerAuthConfig())
}

export async function deleteStaff(userId) {
  await api.delete(`/auth/staff/${userId}`, ownerAuthConfig())
}

function buildMenuItemFormData(payload) {
  const formData = new FormData()

  formData.append('name', payload.name)
  formData.append('price', String(payload.price))
  formData.append('category', payload.category)
  formData.append('is_available', String(payload.is_available))

  if (payload.imageFile instanceof File) {
    formData.append('image', payload.imageFile)
  }

  return formData
}

// Analytics / Reporting
export async function fetchDailySales(days = 7) {
  const response = await api.get(`/reports/daily-sales?days=${days}`, ownerAuthConfig())
  return response.data
}

export async function fetchTopItems(limit = 10) {
  const response = await api.get(`/reports/top-items?limit=${limit}`, ownerAuthConfig())
  return response.data
}

export async function fetchAnalytics() {
  const response = await api.get('/reports/analytics', ownerAuthConfig())
  return response.data
}

