import api from '@/services/api'

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
  const orders = await api.get('/orders')
  return Array.isArray(orders) ? orders.map(normalizeOrder) : []
}

export async function fetchOwnerMenuItems() {
  const menuItems = await api.get('/menus')
  return Array.isArray(menuItems) ? menuItems.map(normalizeMenuItem) : []
}

export async function updateOrderStatus(orderId, status) {
  const order = await api.patch(`/orders/${orderId}/status`, { status })
  return normalizeOrder(order)
}

export async function deleteMenuItem(itemId) {
  await api.delete(`/menus/${itemId}`)
}

export async function createMenuItem(payload) {
  const formData = buildMenuItemFormData(payload)
  const item = await api.post('/menus', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return normalizeMenuItem(item)
}

export async function updateMenuItem(itemId, payload) {
  const formData = buildMenuItemFormData(payload)
  const item = await api.patch(`/menus/${itemId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return normalizeMenuItem(item)
}

export async function fetchUsers() {
  const users = await api.get('/auth/debug/users')
  return Array.isArray(users) ? users : []
}

export async function createStaff(payload) {
  return api.post('/auth/staff', payload)
}

export async function deleteStaff(userId) {
  await api.delete(`/auth/staff/${userId}`)
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
