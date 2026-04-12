<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 class="font-heading text-3xl font-bold text-foreground">Table Management</h1>
          <p class="mt-1 text-sm text-muted-foreground">
            Create tables, print QR access links, and remove unused tables safely.
          </p>
        </div>

        <form class="flex flex-col gap-3 sm:flex-row" @submit.prevent="handleCreateTable">
          <input
            v-model.number="newTableNumber"
            type="number"
            min="1"
            placeholder="Table number"
            class="w-full rounded-xl border border-input bg-card px-4 py-2.5 text-sm text-foreground outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20 sm:w-40"
          >
          <button
            type="submit"
            class="rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="creatingTable"
          >
            {{ creatingTable ? 'Creating...' : 'Add table' }}
          </button>
        </form>
      </div>

      <p
        v-if="errorMessage"
        class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ errorMessage }}
      </p>

      <p
        v-if="successMessage"
        class="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700"
      >
        {{ successMessage }}
      </p>

      <div class="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        <PanelCard title="Default Setup" subtitle="Practical starting point for small restaurants">
          <div class="space-y-3 text-sm text-muted-foreground">
            <p>New databases now start with 10 tables instead of 20.</p>
            <p>Add more only when the floor actually needs them to keep the QR list manageable.</p>
            <p>Tables with order history cannot be deleted, which protects reporting and past order links.</p>
          </div>
        </PanelCard>

        <PanelCard title="Order Flow" subtitle="How table orders are managed automatically">
          <div class="space-y-3 text-sm text-muted-foreground">
            <p><strong class="text-foreground">Active Orders:</strong> Customers can add items to their unpaid order even after leaving the page.</p>
            <p><strong class="text-foreground">Auto-Clear:</strong> When you mark payment as PAID, the order closes and table becomes AVAILABLE.</p>
            <p><strong class="text-foreground">History:</strong> All orders are preserved forever for reporting. Next customer gets a fresh order.</p>
          </div>
        </PanelCard>

        <PanelCard title="Current Tables" subtitle="Live count of configured customer entry points">
          <div class="flex items-end justify-between">
            <div>
              <p class="text-4xl font-semibold text-foreground">{{ tables.length }}</p>
              <p class="mt-2 text-sm text-muted-foreground">Configured tables</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-foreground">{{ occupiedCount }}</p>
              <p class="mt-1 text-xs uppercase tracking-[0.2em] text-muted-foreground">Occupied</p>
            </div>
          </div>
        </PanelCard>
      </div>

      <div v-if="loading" class="text-sm text-muted-foreground">Loading tables...</div>

      <div v-else class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <section
          v-for="table in tables"
          :key="table.id"
          class="rounded-3xl border border-border bg-card p-5 shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-xs uppercase tracking-[0.22em] text-muted-foreground">Table</p>
              <h2 class="mt-2 text-3xl font-semibold text-foreground">{{ table.number }}</h2>
            </div>
            <StatusBadge :status="table.status" />
          </div>

          <div class="mt-4 overflow-hidden rounded-2xl border border-border bg-white p-4">
            <img
              :src="table.qrImage"
              :alt="`Table ${table.number} QR code`"
              class="mx-auto aspect-square w-full max-w-[200px]"
            >
          </div>

          <div class="mt-4 rounded-2xl bg-muted/60 px-4 py-3">
            <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Direct link</p>
            <p class="mt-2 break-all text-sm text-foreground">{{ table.orderUrl }}</p>
          </div>

          <div v-if="table.orderCount > 0" class="mt-4 grid grid-cols-2 gap-3 rounded-2xl bg-blue-50 px-4 py-3">
            <div>
              <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Total Orders</p>
              <p class="mt-1 text-2xl font-semibold text-foreground">{{ table.orderCount }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Paid</p>
              <p class="mt-1 text-2xl font-semibold text-green-700">{{ table.paidOrderCount }}</p>
            </div>
          </div>

          <div class="mt-4 grid gap-2 sm:grid-cols-2">
            <button
              type="button"
              class="rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
              @click="copyTableLink(table)"
            >
              Copy link
            </button>
            <a
              :href="table.orderUrl"
              target="_blank"
              rel="noreferrer"
              class="rounded-xl border border-border px-4 py-2.5 text-center text-sm font-medium text-foreground transition hover:bg-accent"
            >
              Open
            </a>
          </div>

          <button
            type="button"
            class="mt-3 w-full rounded-xl border border-red-200 px-4 py-2.5 text-sm font-medium text-red-700 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="deletingTableNumber === table.number"
            @click="handleDeleteTable(table)"
          >
            {{ deletingTableNumber === table.number ? 'Deleting...' : 'Delete table' }}
          </button>
        </section>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import QRCode from 'qrcode'

import DashboardLayout from '@/components/DashboardLayout.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { createTable, deleteTable, fetchTableAccessLinks, fetchOwnerOrders } from '@/services/owner'

const tables = ref([])
const allOrders = ref([])
const loading = ref(false)
const creatingTable = ref(false)
const deletingTableNumber = ref(null)
const newTableNumber = ref(11)
const errorMessage = ref('')
const successMessage = ref('')

const occupiedCount = computed(() => {
  return tables.value.filter((table) => String(table.status).toLowerCase() === 'occupied').length
})

onMounted(() => {
  loadTables()
})

async function loadTables() {
  loading.value = true
  errorMessage.value = ''

  try {
    const [loadedTables, orders] = await Promise.all([
      fetchTableAccessLinks(),
      fetchOwnerOrders()
    ])
    
    allOrders.value = orders
    
    tables.value = await Promise.all(
      loadedTables.map(async (table) => {
        const orderUrl = buildTableOrderUrl(table)
        const tableOrders = orders.filter(order => order.table?.number === table.number)
        const paidOrders = tableOrders.filter(order => 
          String(order.paymentStatus).toLowerCase() === 'paid'
        )
        
        return {
          ...table,
          orderUrl,
          orderCount: tableOrders.length,
          paidOrderCount: paidOrders.length,
          qrImage: await QRCode.toDataURL(orderUrl, {
            margin: 1,
            width: 360,
            color: {
              dark: '#2d1f17',
              light: '#ffffff',
            },
          }),
        }
      })
    )

    const highestTableNumber = tables.value.reduce((max, table) => Math.max(max, table.number), 0)
    newTableNumber.value = highestTableNumber + 1
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not load tables.'
  } finally {
    loading.value = false
  }
}

async function handleCreateTable() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!Number.isInteger(newTableNumber.value) || newTableNumber.value <= 0) {
    errorMessage.value = 'Enter a valid table number greater than 0.'
    return
  }

  creatingTable.value = true

  try {
    await createTable(newTableNumber.value)
    successMessage.value = `Table ${newTableNumber.value} created.`
    await loadTables()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not create table.'
  } finally {
    creatingTable.value = false
  }
}

async function handleDeleteTable(table) {
  errorMessage.value = ''
  successMessage.value = ''
  deletingTableNumber.value = table.number

  try {
    await deleteTable(table.number)
    successMessage.value = `Table ${table.number} deleted.`
    await loadTables()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not delete table.'
  } finally {
    deletingTableNumber.value = null
  }
}

function buildTableOrderUrl(table) {
  const url = new URL(`/table/${table.number}`, window.location.origin)
  url.searchParams.set('token', table.qr_token)
  return url.toString()
}

async function copyTableLink(table) {
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await navigator.clipboard.writeText(table.orderUrl)
    successMessage.value = `Copied table ${table.number} link.`
  } catch {
    errorMessage.value = 'Could not copy the table link.'
  }
}
</script>
