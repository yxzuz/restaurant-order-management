<template>
  <div class="min-h-screen bg-background pb-20">
    <!-- Sticky Header -->
    <header class="sticky top-0 z-30 bg-card border-b">
      <div class="container flex items-center justify-between h-12 sm:h-14 px-3 sm:px-4">
        <div class="flex items-center gap-2 sm:gap-3">
          <router-link to="/">
            <Button variant="ghost" size="icon" class="h-7 w-7 sm:h-8 sm:w-8">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sm:w-4 sm:h-4">
                <path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>
              </svg>
            </Button>
          </router-link>
          <div class="flex items-center gap-1.5 sm:gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary sm:w-5 sm:h-5">
              <path d="m16 2-2.3 2.3a3 3 0 0 0 0 4.2l1.8 1.8a3 3 0 0 0 4.2 0L22 8"/><path d="M15 15 3.3 3.3a4.2 4.2 0 0 0 0 6l7.3 7.3c.7.7 2 .7 2.8 0L15 15Zm0 0 7 7"/><path d="m2.1 21.8 6.4-6.3"/><path d="m19 5-7 7"/>
            </svg>
            <span class="font-semibold text-sm sm:text-base">Table {{ tableNumber }}</span>
          </div>
        </div>
        <div class="flex items-center gap-1.5 sm:gap-2">
          <Button 
            v-if="activeOrder" 
            variant="outline" 
            size="sm" 
            @click="orderHistoryOpen = true"
            class="text-[10px] sm:text-xs px-2 sm:px-3 h-7 sm:h-8"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-0.5 sm:mr-1 sm:w-3.5 sm:h-3.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
            </svg>
            <span class="hidden sm:inline">My Order</span>
            <span class="sm:hidden">Order</span>
          </Button>
          <Button variant="outline" size="icon" class="relative h-7 w-7 sm:h-9 sm:w-9" @click="cartDrawerOpen = true">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sm:w-4 sm:h-4">
              <circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
            </svg>
            <Badge v-if="cartItemCount > 0" class="absolute -top-1.5 -right-1.5 sm:-top-2 sm:-right-2 h-4 w-4 sm:h-5 sm:w-5 p-0 flex items-center justify-center text-[9px] sm:text-[10px]">
              {{ cartItemCount }}
            </Badge>
          </Button>
        </div>
      </div>
    </header>

    <section class="container px-3 sm:px-4 py-3 sm:py-4">
      <!-- Error Message -->
      <div
        v-if="pageError"
        class="mb-3 sm:mb-4 rounded-xl sm:rounded-2xl border border-red-200 bg-red-50 px-3 sm:px-4 py-2.5 sm:py-3 text-xs sm:text-sm text-red-700"
      >
        {{ pageError }}
      </div>

      <!-- QR Required Message -->
      <div
        v-if="requiresQrAccess"
        class="rounded-2xl sm:rounded-3xl border border-border bg-card p-6 sm:p-8 shadow-sm"
      >
        <p class="text-xs sm:text-sm font-semibold uppercase tracking-[0.28em] text-orange-600">
          QR required
        </p>
        <h2 class="mt-2 sm:mt-3 text-2xl sm:text-3xl font-semibold text-foreground">
          Scan the table QR code first.
        </h2>
        <p class="mt-3 sm:mt-4 max-w-2xl text-sm sm:text-base leading-6 sm:leading-7 text-muted-foreground">
          This page needs a valid table token from the QR code so the order is attached to the correct table.
        </p>
        <div class="mt-5 sm:mt-6 flex flex-col sm:flex-row flex-wrap gap-2 sm:gap-3">
          <router-link
            to="/customer"
            class="text-center rounded-xl sm:rounded-2xl bg-primary px-4 sm:px-5 py-2.5 sm:py-3 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          >
            Go to QR access page
          </router-link>
          <router-link
            to="/"
            class="text-center rounded-xl sm:rounded-2xl border border-border px-4 sm:px-5 py-2.5 sm:py-3 text-sm font-medium text-foreground transition hover:bg-accent"
          >
            Back to home
          </router-link>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else>
        <!-- Loading State -->
        <div
          v-if="loading"
          class="rounded-3xl border border-dashed border-border bg-card px-6 py-16 text-center text-sm text-muted-foreground"
        >
          Loading table menu...
        </div>

        <template v-else>
          <!-- Category Filters -->
          <div class="flex gap-1.5 sm:gap-2 overflow-x-auto pb-2 mb-3 sm:mb-4 scrollbar-none">
            <Button
              v-for="category in categories"
              :key="category"
              :variant="selectedCategory === category ? 'default' : 'outline'"
              size="sm"
              @click="selectedCategory = category"
              class="shrink-0 text-xs sm:text-sm px-3 sm:px-4 h-8 sm:h-9"
            >
              {{ category }}
            </Button>
          </div>

          <!-- Menu Items -->
          <div
            v-if="filteredMenuItems.length === 0"
            class="rounded-2xl sm:rounded-3xl border border-dashed border-border bg-card px-4 sm:px-6 py-12 sm:py-16 text-center text-xs sm:text-sm text-muted-foreground"
          >
            No dishes found for this category.
          </div>
          <div v-else class="grid gap-2 sm:gap-2.5 grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            <CustomerMenuItemCard
              v-for="item in filteredMenuItems"
              :key="item.id"
              :item="item"
              :quantity="getQuantity(item.id)"
              @add="addItem"
              @remove="removeItem"
            />
          </div>
        </template>
      </div>
    </section>

    <!-- Floating Cart Bar -->
    <div v-if="cartItemCount > 0 && !requiresQrAccess" class="fixed bottom-0 left-0 right-0 bg-card border-t p-4 z-20">
      <Button class="w-full" size="lg" @click="cartDrawerOpen = true">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
          <circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
        </svg>
        View Cart ({{ cartItemCount }}) — {{ formatCurrency(cartTotal) }}
      </Button>
    </div>

    <!-- Order History Drawer -->
    <Transition name="drawer">
      <div v-if="orderHistoryOpen" class="fixed inset-0 z-50 flex justify-end" @click.self="orderHistoryOpen = false">
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/50" @click="orderHistoryOpen = false"></div>
        
        <!-- Drawer Content -->
        <div class="relative w-full max-w-md bg-card h-full shadow-lg flex flex-col">
          <div class="p-6 border-b flex items-center justify-between">
            <h2 class="text-lg font-semibold">My Order</h2>
            <Button variant="ghost" size="icon" @click="orderHistoryOpen = false">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
              </svg>
            </Button>
          </div>

          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="!activeOrder" class="text-muted-foreground text-sm text-center py-8">
              You haven't placed an order yet
            </div>
            
            <div v-else class="space-y-4">
              <div class="rounded-2xl border border-border bg-muted/30 p-4">
                <div class="flex items-center justify-between mb-3">
                  <div>
                    <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Order Number</p>
                    <p class="text-lg font-bold mt-1">#{{ activeOrder.id }}</p>
                  </div>
                  <StatusBadge :status="activeOrder.status" />
                </div>
                <div class="text-xs text-muted-foreground">
                  <p>Placed: {{ formatDate(activeOrder.created_at) }}</p>
                  <p v-if="activeOrder.updated_at !== activeOrder.created_at">
                    Updated: {{ formatDate(activeOrder.updated_at) }}
                  </p>
                </div>
              </div>

              <div class="space-y-3">
                <p class="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Order Items</p>
                <div 
                  v-for="item in activeOrder.items" 
                  :key="item.id" 
                  class="flex flex-col gap-2 bg-card rounded-lg border p-3"
                >
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <div class="flex items-center gap-2 mb-1">
                        <p class="font-medium text-sm">{{ item.menu_item?.name || `Item #${item.menu_item_id}` }}</p>
                        <StatusBadge :status="item.status || 'NEW'" />
                      </div>
                      <p class="text-xs text-muted-foreground">{{ formatCurrency(item.unit_price) }} × {{ item.quantity }}</p>
                    </div>
                    <div class="text-right">
                      <p class="font-semibold text-sm">{{ formatCurrency(item.unit_price * item.quantity) }}</p>
                    </div>
                  </div>
                  <button
                    v-if="canCancelItem(item) && !cancellingItem"
                    type="button"
                    class="rounded-lg border border-destructive/30 px-3 py-1.5 text-xs font-semibold text-destructive transition hover:bg-destructive/10"
                    @click="cancelItem(item)"
                  >
                    ✕ Cancel this item
                  </button>
                </div>
              </div>

              <div class="border-t pt-4">
                <div class="flex justify-between items-center mb-2">
                  <span class="font-semibold text-lg">Total Amount</span>
                  <span class="text-2xl font-bold text-primary">{{ formatCurrency(activeOrder.total_amount) }}</span>
                </div>
                <div class="rounded-lg bg-blue-50 border border-blue-200 px-3 py-2.5 mt-3">
                  <p class="text-xs text-blue-900">
                    <strong>Order Status:</strong> {{ getOrderStatusSummary() }}
                  </p>
                  <p class="text-xs text-blue-700 mt-1">
                    Our staff will collect payment when you're ready to leave.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="border-t p-6">
            <Button 
              variant="outline" 
              class="w-full" 
              @click="orderHistoryOpen = false"
            >
              Continue Browsing Menu
            </Button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Cart Drawer -->
    <Transition name="drawer">
      <div v-if="cartDrawerOpen" class="fixed inset-0 z-50 flex justify-end" @click.self="cartDrawerOpen = false">
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/50" @click="cartDrawerOpen = false"></div>
        
        <!-- Drawer Content -->
        <div class="relative w-full max-w-md bg-card h-full shadow-lg flex flex-col">
          <div class="p-6 border-b flex items-center justify-between">
            <h2 class="text-lg font-semibold">Your Cart</h2>
            <Button variant="ghost" size="icon" @click="cartDrawerOpen = false">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
              </svg>
            </Button>
          </div>

          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="cart.length === 0" class="text-muted-foreground text-sm text-center py-8">
              Your cart is empty
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="item in cart" :key="item.id" class="flex justify-between items-center">
                <div class="flex-1">
                  <p class="font-medium text-sm">{{ item.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.quantity }} × {{ formatCurrency(item.price) }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-sm">{{ formatCurrency(item.price * item.quantity) }}</span>
                  <Button variant="ghost" size="icon" class="h-6 w-6" @click="removeLine(item.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
                    </svg>
                  </Button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="cart.length > 0" class="border-t p-6">
            <div class="flex justify-between font-semibold mb-4">
              <span>Total</span>
              <span>{{ formatCurrency(cartTotal) }}</span>
            </div>

            <p
              v-if="submitError"
              class="mb-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {{ submitError }}
            </p>

            <p
              v-if="submitSuccessMessage"
              class="mb-4 rounded-2xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700"
            >
              {{ submitSuccessMessage }}
            </p>

            <Button 
              class="w-full" 
              @click="submitOrder"
              :disabled="cart.length === 0 || submitting || !qrToken"
            >
              {{ submitting ? 'Sending order...' : activeOrder ? 'Add items to current order' : 'Place Order' }}
            </Button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import CustomerMenuItemCard from '@/components/CustomerMenuItemCard.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { createCustomerOrder, fetchActiveOrderForTable, fetchCustomerMenuItems, cancelCustomerOrderItem } from '@/services/customer'

const route = useRoute()

const menuItems = ref([])
const activeOrder = ref(null)
const cart = ref([])
const loading = ref(false)
const submitting = ref(false)
const cancellingItem = ref(false)
const pageError = ref('')
const submitError = ref('')
const submitSuccessMessage = ref('')
const selectedCategory = ref('All')
const cartDrawerOpen = ref(false)
const orderHistoryOpen = ref(false)

let refreshTimer = null

const tableNumber = computed(() => Number(route.params.tableNumber))
const routeQrToken = computed(() => {
  const token = route.query.token
  return typeof token === 'string' ? token : ''
})

const qrToken = computed(() => {
  if (routeQrToken.value) {
    return routeQrToken.value
  }

  if (!Number.isInteger(tableNumber.value) || tableNumber.value <= 0) {
    return ''
  }

  return window.localStorage.getItem(getTableTokenStorageKey(tableNumber.value)) || ''
})
const requiresQrAccess = computed(() => !loading.value && !qrToken.value)

const categories = computed(() => {
  const distinctCategories = [...new Set(menuItems.value.map((item) => item.category).filter(Boolean))]
  return ['All', ...distinctCategories]
})

const filteredMenuItems = computed(() => {
  if (selectedCategory.value === 'All') {
    return menuItems.value
  }

  return menuItems.value.filter((item) => item.category === selectedCategory.value)
})

const availableItemsCount = computed(() => menuItems.value.filter((item) => item.is_available).length)

const cartItemCount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.quantity, 0)
})

const cartTotal = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

onMounted(() => {
  persistRouteToken()
  loadPageData()
  startAutoRefresh()
})

onBeforeUnmount(() => {
  stopAutoRefresh()
})

watch(
  () => [route.params.tableNumber, route.query.token],
  () => {
    persistRouteToken()
    resetTransientState()
    loadPageData()
  }
)

function getTableTokenStorageKey(tableNo) {
  return `table_qr_token:${tableNo}`
}

function persistRouteToken() {
  if (!routeQrToken.value || !Number.isInteger(tableNumber.value) || tableNumber.value <= 0) {
    return
  }

  window.localStorage.setItem(getTableTokenStorageKey(tableNumber.value), routeQrToken.value)
}

function resetTransientState() {
  pageError.value = ''
  submitError.value = ''
  submitSuccessMessage.value = ''
  activeOrder.value = null
  cart.value = []
}

async function loadPageData() {
  loading.value = true
  pageError.value = ''

  if (!Number.isInteger(tableNumber.value) || tableNumber.value <= 0) {
    pageError.value = 'Invalid table number.'
    loading.value = false
    return
  }

  if (!qrToken.value) {
    pageError.value = ''
    loading.value = false
    return
  }

  try {
    const [menu, order] = await Promise.all([
      fetchCustomerMenuItems(tableNumber.value, qrToken.value),
      fetchActiveOrderForTable(tableNumber.value, qrToken.value),
    ])

    menuItems.value = menu
    activeOrder.value = order

    if (!categories.value.includes(selectedCategory.value)) {
      selectedCategory.value = 'All'
    }
  } catch (error) {
    pageError.value = error?.response?.data?.detail || error?.message || 'Could not load this table.'
  } finally {
    loading.value = false
  }
}

async function refreshActiveOrder() {
  submitError.value = ''

  try {
    activeOrder.value = await fetchActiveOrderForTable(tableNumber.value, qrToken.value)
  } catch (error) {
    pageError.value = error?.response?.data?.detail || 'Could not refresh order status.'
  }
}

function startAutoRefresh() {
  refreshTimer = window.setInterval(() => {
    if (!qrToken.value || loading.value || submitting.value) {
      return
    }

    refreshActiveOrder()
  }, 5000) // Refresh every 5 seconds for real-time updates
}

function stopAutoRefresh() {
  if (refreshTimer) {
    window.clearInterval(refreshTimer)
    refreshTimer = null
  }
}

function getQuantity(itemId) {
  return cart.value.find((item) => item.id === itemId)?.quantity ?? 0
}

function addItem(menuItem) {
  submitSuccessMessage.value = ''
  const existingItem = cart.value.find((item) => item.id === menuItem.id)

  if (existingItem) {
    existingItem.quantity += 1
    return
  }

  cart.value = [
    ...cart.value,
    {
      id: menuItem.id,
      menu_item_id: menuItem.id,
      name: menuItem.name,
      price: Number(menuItem.price),
      quantity: 1,
    },
  ]
}

function removeItem(menuItem) {
  submitSuccessMessage.value = ''
  const existingItem = cart.value.find((item) => item.id === menuItem.id)
  if (!existingItem) {
    return
  }

  if (existingItem.quantity === 1) {
    removeLine(menuItem.id)
    return
  }

  existingItem.quantity -= 1
}

function removeLine(itemId) {
  submitSuccessMessage.value = ''
  cart.value = cart.value.filter((item) => item.id !== itemId)
}

async function submitOrder() {
  if (cart.value.length === 0 || !qrToken.value) {
    return
  }

  submitting.value = true
  submitError.value = ''
  submitSuccessMessage.value = ''

  try {
    const order = await createCustomerOrder({
      tableNumber: tableNumber.value,
      qrToken: qrToken.value,
      items: cart.value,
    })

    activeOrder.value = order
    cart.value = []
    submitSuccessMessage.value = activeOrder.value
      ? 'Your items were sent to the kitchen.'
      : 'Your order was placed.'
    
    // Close drawer after a short delay to show success message
    setTimeout(() => {
      cartDrawerOpen.value = false
      submitSuccessMessage.value = ''
    }, 2000)
  } catch (error) {
    submitError.value = error?.response?.data?.detail || 'Could not send your order.'
  } finally {
    submitting.value = false
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(Number(value) || 0)
}

function formatStatus(value) {
  return String(value || '')
    .replace(/_/g, ' ')
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

function formatDate(value) {
  if (!value) {
    return 'just now'
  }

  return new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Bangkok',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(new Date(value))
}

function getOrderStatusSummary() {
  if (!activeOrder.value || !activeOrder.value.items || activeOrder.value.items.length === 0) {
    return 'No items'
  }

  const items = activeOrder.value.items
  const statusCounts = items.reduce((acc, item) => {
    const status = String(item.status || 'NEW').toUpperCase()
    acc[status] = (acc[status] || 0) + 1
    return acc
  }, {})

  const total = items.length
  
  if (statusCounts.COMPLETED === total) {
    return 'All items ready!'
  }
  
  if (statusCounts.READY) {
    return `${statusCounts.READY} of ${total} items ready`
  }
  
  if (statusCounts.PREPARING) {
    return `${statusCounts.PREPARING} of ${total} items being prepared`
  }
  
  return 'Order received - Kitchen notified'
}

function canCancelItem(item) {
  const itemStatus = String(item.status || 'NEW').toUpperCase()
  const isPaid = activeOrder.value?.payment_status?.toLowerCase() === 'paid'
  return !isPaid && itemStatus === 'NEW'
}

async function cancelItem(item) {
  if (!activeOrder.value || cancellingItem.value) {
    return
  }

  cancellingItem.value = true
  pageError.value = ''

  try {
    const updatedOrder = await cancelCustomerOrderItem(activeOrder.value.id, item.id, qrToken.value)
    activeOrder.value = updatedOrder
    
    // Close drawer if no items left
    if (!updatedOrder.items || updatedOrder.items.length === 0) {
      orderHistoryOpen.value = false
    }
  } catch (error) {
    pageError.value = error?.response?.data?.detail || 'Could not cancel item. It may have already been started.'
  } finally {
    cancellingItem.value = false
  }
}
</script>

<style scoped>
/* Drawer transition animations */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.3s ease;
}

.drawer-enter-active > div:last-child,
.drawer-leave-active > div:last-child {
  transition: transform 0.3s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from > div:last-child,
.drawer-leave-to > div:last-child {
  transform: translateX(100%);
}
</style>
