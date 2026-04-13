import api from '@/services/api'
import { normalizeMenuItem, normalizeOrder } from '@/services/owner'

export async function fetchCustomerMenuItems(tableNumber, qrToken) {
  if (!tableNumber || !qrToken) {
    throw new Error('Table number and QR token are required to view the menu.')
  }

  const menuItems = await api.get(`/tables/${tableNumber}/menu`, {
    params: { qr_token: qrToken },
  })
  return Array.isArray(menuItems) ? menuItems.map(normalizeMenuItem) : []
}

export async function fetchActiveOrderForTable(tableNumber, qrToken) {
  if (!qrToken) {
    throw new Error('QR token is required to access this table.')
  }

  const order = await api.get(`/tables/${tableNumber}/active-order`, {
    params: { qr_token: qrToken },
  })

  return order ? normalizeOrder(order) : null
}

export async function createCustomerOrder({ tableNumber, qrToken, items }) {
  const order = await api.post('/orders', {
    table_number: Number(tableNumber),
    qr_token: qrToken,
    items: items.map((item) => ({
      menu_item_id: item.menu_item_id,
      quantity: item.quantity,
    })),
  })

  return normalizeOrder(order)
}

export async function cancelCustomerOrderItem(orderId, itemId, qrToken) {
  if (!qrToken) {
    throw new Error('QR token is required to cancel items for this table.')
  }

  const order = await api.delete(`/orders/${orderId}/items/${itemId}`, {
    params: { qr_token: qrToken },
  })
  return normalizeOrder(order)
}
