<template>
  <DashboardLayout role="owner">
    <div class="space-y-4 sm:space-y-6">
      <div>
        <h1 class="font-heading text-2xl sm:text-3xl font-bold text-foreground">Dashboard</h1>
        <p class="mt-1 text-xs sm:text-sm text-muted-foreground">Overview of today's operations</p>
      </div>

      <p
        v-if="errorMessage"
        class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ errorMessage }}
      </p>

      <div class="grid gap-3 sm:gap-4 grid-cols-2 lg:grid-cols-4">
        <StatCard
          v-for="stat in stats"
          :key="stat.title"
          :title="stat.title"
          :value="stat.value"
          :icon="stat.icon"
          :description="stat.description"
        />
      </div>

      <div class="grid gap-3 sm:gap-4 lg:grid-cols-2">
        <PanelCard title="Recent Orders" subtitle="Live kitchen and floor activity">
          <div class="space-y-2 sm:space-y-3">
            <div
              v-for="order in recentOrders"
              :key="order.id"
              class="flex items-center justify-between rounded-xl sm:rounded-2xl border border-border/70 px-3 sm:px-4 py-2 sm:py-3"
            >
              <div>
                <p class="text-xs sm:text-sm font-semibold text-foreground">Table {{ order.table_number }}</p>
                <p class="mt-1 text-[10px] sm:text-xs text-muted-foreground">{{ order.items.length }} items</p>
              </div>
              <div class="text-right">
                <p class="text-xs sm:text-sm font-semibold text-foreground">{{ formatCurrency(order.total_amount) }}</p>
                <div class="mt-1 sm:mt-2">
                  <StatusBadge :status="order.status" />
                </div>
              </div>
            </div>
          </div>
        </PanelCard>

        <PanelCard title="Popular Items" subtitle="Top menu items for today">
          <div class="space-y-2 sm:space-y-3">
            <div
              v-for="(item, index) in popularItems"
              :key="item.id"
              class="flex items-center justify-between rounded-xl sm:rounded-2xl border border-border/70 px-3 sm:px-4 py-2 sm:py-3"
            >
              <div class="flex items-center gap-2 sm:gap-4">
                <span class="font-heading text-xl sm:text-2xl font-bold text-muted-foreground">#{{ index + 1 }}</span>
                <div>
                  <p class="text-xs sm:text-sm font-semibold text-foreground">{{ item.name }}</p>
                  <p class="mt-1 text-[10px] sm:text-xs text-muted-foreground">{{ item.category }}</p>
                </div>
              </div>
              <p class="text-xs sm:text-sm font-semibold text-foreground">{{ formatCurrency(item.price) }}</p>
            </div>
          </div>
        </PanelCard>
      </div>

      <PanelCard title="Table QR Codes" subtitle="Scan opens the direct customer ordering link">
        <div v-if="tableLinks.length === 0" class="text-xs sm:text-sm text-muted-foreground">
          No table QR codes available.
        </div>

        <div v-else class="grid gap-3 sm:gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          <div
            v-for="table in tableLinks"
            :key="table.id"
            class="rounded-2xl sm:rounded-3xl border border-border/70 bg-background p-3 sm:p-4"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-[10px] sm:text-xs uppercase tracking-[0.2em] text-muted-foreground">Table</p>
                <p class="mt-1 text-xl sm:text-2xl font-semibold text-foreground">{{ table.number }}</p>
              </div>
              <StatusBadge :status="table.status" />
            </div>

            <div class="mt-3 sm:mt-4 overflow-hidden rounded-xl sm:rounded-2xl border border-border bg-white p-2 sm:p-3">
              <img
                :src="table.qrImage"
                :alt="`Table ${table.number} QR code`"
                class="mx-auto aspect-square w-full max-w-[180px]"
              >
            </div>

            <div class="mt-3 sm:mt-4 space-y-1.5 sm:space-y-2">
              <button
                type="button"
                class="w-full rounded-lg sm:rounded-xl bg-primary px-3 sm:px-4 py-2 text-xs sm:text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
                @click="copyTableLink(table)"
              >
                Copy link
              </button>
              <a
                :href="table.orderUrl"
                target="_blank"
                rel="noreferrer"
                class="block w-full rounded-xl border border-border px-4 py-2 text-center text-sm font-medium text-foreground transition hover:bg-accent"
              >
                Open link
              </a>
            </div>
          </div>
        </div>
      </PanelCard>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, h, onMounted, ref } from 'vue'
import { DollarSign, ShoppingBag, Clock, TrendingUp } from 'lucide-vue-next'
import QRCode from 'qrcode'

import DashboardLayout from '@/components/DashboardLayout.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { fetchOwnerMenuItems, fetchOwnerOrders, fetchTableAccessLinks } from '@/services/owner'

const orders = ref([])
const menuItems = ref([])
const tableLinks = ref([])
const errorMessage = ref('')

onMounted(() => {
  loadDashboard()
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(value)
}

const formatBahtCompact = (value) => {
  const numeric = Number(value) || 0
  const compact = new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(numeric)
  return `${compact}`
}

const BahtIcon = {
  render() {
    return h('span', { class: 'text-lg font-bold leading-none' }, '฿')
  },
}

const stats = computed(() => [
  {
    title: 'Total Revenue',
    value: formatBahtCompact(orders.value.reduce((sum, order) => sum + Number(order.total_amount), 0)),
    icon: BahtIcon,
    description: "Today's earnings",
  },
  {
    title: 'Active Orders',
    value: orders.value.filter((order) => !['completed', 'cancelled'].includes(String(order.status).toLowerCase())).length,
    icon: Clock,
    description: 'Currently in progress',
  },
  {
    title: 'Total Orders',
    value: orders.value.length,
    icon: ShoppingBag,
    description: 'Orders today',
  },
  {
    title: 'Menu Items',
    value: menuItems.value.filter((item) => item.is_available).length,
    icon: TrendingUp,
    description: 'Items available',
  },
])

const recentOrders = computed(() => orders.value.slice(0, 5))

const popularItems = computed(() => {
  const sales = {}

  orders.value.forEach((order) => {
    order.items.forEach((item) => {
      const name = item.menu_item?.name || 'Menu item'
      sales[name] = (sales[name] || 0) + Number(item.quantity)
    })
  })

  return [...menuItems.value]
    .sort((a, b) => (sales[b.name] || 0) - (sales[a.name] || 0))
    .slice(0, 5)
})

async function loadDashboard() {
  errorMessage.value = ''

  try {
    const [loadedOrders, loadedMenuItems, loadedTables] = await Promise.all([
      fetchOwnerOrders(),
      fetchOwnerMenuItems(),
      fetchTableAccessLinks(),
    ])

    orders.value = loadedOrders
    menuItems.value = loadedMenuItems
    tableLinks.value = await Promise.all(
      loadedTables.map(async (table) => {
        const orderUrl = buildTableOrderUrl(table)
        return {
          ...table,
          orderUrl,
          qrImage: await QRCode.toDataURL(orderUrl, {
            margin: 1,
            width: 320,
            color: {
              dark: '#2d1f17',
              light: '#ffffff',
            },
          }),
        }
      })
    )
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not load dashboard data.'
  }
}

function buildTableOrderUrl(table) {
  const url = new URL(`/table/${table.number}`, window.location.origin)
  url.searchParams.set('token', table.qr_token)
  return url.toString()
}

async function copyTableLink(table) {
  try {
    await navigator.clipboard.writeText(table.orderUrl)
  } catch {
    errorMessage.value = 'Could not copy the table link.'
  }
}
</script>
