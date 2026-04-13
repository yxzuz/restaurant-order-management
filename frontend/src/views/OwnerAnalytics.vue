<template>
  <DashboardLayout role="owner">
    <div class="py-4 sm:py-5 space-y-3 sm:space-y-4">

    <!-- Header + tab toggle -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
      <p class="text-base sm:text-lg font-medium text-foreground">Overview</p>
      <div class="flex gap-1 bg-muted/50 p-1 rounded-lg border border-border/50">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab-btn', { active: currentTab === tab.key }]"
          @click="currentTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Metric cards -->
    <div class="grid gap-3 sm:gap-4 grid-cols-2 lg:grid-cols-4">
      <StatCard
        v-for="m in metrics"
        :key="m.title"
        :title="m.title"
        :value="m.value"
        :description="`${m.delta} vs ${currentTab === 'today' ? 'yesterday' : 'last month'}`"
        :icon="m.icon"
      />
    </div>

    <div class="grid gap-3 sm:gap-4 lg:grid-cols-2">
      <!-- Revenue chart -->
      <div class="card">
        <p class="section-title">{{ currentTab === 'today' ? 'Revenue by hour' : 'Revenue by week' }}</p>
        <div class="relative h-32 sm:h-40">
          <svg class="w-full h-[120px] sm:h-[130px]" viewBox="0 0 400 120" preserveAspectRatio="none">
            <defs>
              <linearGradient id="ag" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" :stop-color="chartColor" stop-opacity="0.15"/>
                <stop offset="100%" :stop-color="chartColor" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <line x1="0" y1="0"   x2="400" y2="0"   stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
            <line x1="0" y1="40"  x2="400" y2="40"  stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
            <line x1="0" y1="80"  x2="400" y2="80"  stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
            <line x1="0" y1="119" x2="400" y2="119" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
            <path :d="chartPaths.area" fill="url(#ag)"/>
            <path :d="chartPaths.line" fill="none" :stroke="chartColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <div class="flex justify-between mt-1">
            <span v-for="l in chartXLabels" :key="l" class="text-[10px] sm:text-xs text-muted-foreground">{{ l }}</span>
          </div>
        </div>
      </div>

      <!-- Status breakdown -->
      <div class="card">
        <p class="section-title">Order status breakdown</p>
        <div>
          <div v-for="s in activeStatus" :key="s.label" class="bar-row">
            <span class="bar-label">{{ s.label }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: s.pct + '%', background: s.color }" />
            </div>
            <span class="bar-val">{{ s.val }}</span>
          </div>
        </div>
        <div class="flex items-center gap-3 sm:gap-4 mt-3 flex-wrap">
          <div :style="{ background: donutGradient }" class="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex-shrink-0" />
          <div class="text-xs sm:text-sm text-muted-foreground leading-relaxed">
            <div v-for="s in activeStatus" :key="s.label">
              <span :style="{ color: s.color }">●</span> {{ s.pct }}% {{ s.label.toLowerCase() }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Orders volume bar chart -->
    <div class="card">
      <p class="section-title">{{ currentTab === 'today' ? 'Orders per day this week' : 'Orders per week this month' }}</p>
      <p v-if="sourceOrders.length === 0" class="text-xs sm:text-sm text-muted-foreground mb-2">
        No orders found. Create some orders to see data.
      </p>
      <div class="flex items-end gap-1.5 sm:gap-2 h-24 sm:h-28">
        <div v-for="b in volumeBars" :key="b.label" class="flex-1 flex flex-col items-center gap-1 sm:gap-1.5">
          <span class="text-[10px] sm:text-xs text-muted-foreground">{{ b.val }}</span>
          <div class="w-full bg-muted/50 rounded-sm sm:rounded h-16 sm:h-20 flex items-end overflow-hidden">
            <div :style="{ height: b.val === 0 ? '2%' : Math.round(b.val / b.max * 100) + '%', background: b.val === 0 ? 'var(--color-border-tertiary)' : chartColor }" class="w-full rounded-t opacity-85" />
          </div>
          <span class="text-[9px] sm:text-[10px] text-muted-foreground truncate w-full text-center">{{ b.label }}</span>
        </div>
      </div>
    </div>

    <!-- Top Selling Items -->
    <div class="card" v-if="topItems.length">
      <p class="section-title">Top Selling Items</p>
      <div class="flex flex-col gap-2 sm:gap-2.5">
        <div v-for="(item, idx) in topItems.slice(0, 5)" :key="item.id" 
             class="flex items-center gap-2 sm:gap-3 p-2 sm:p-3 bg-muted/30 rounded-lg">
          <span class="text-sm sm:text-base font-semibold text-muted-foreground w-5 sm:w-6 text-center">
            {{ idx + 1 }}
          </span>
          <div class="flex-1 min-w-0">
            <div class="text-xs sm:text-sm font-medium text-foreground truncate">
              {{ item.name }}
            </div>
            <div class="text-[10px] sm:text-xs text-muted-foreground">
              {{ item.total_quantity }} sold • {{ item.category }}
            </div>
          </div>
          <div class="text-right shrink-0">
            <div class="text-sm sm:text-base font-semibold text-primary">
              {{ formatCurrency(item.total_revenue) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Revenue by Category -->
    <div class="card" v-if="categoryRevenue.length">
      <p class="section-title">Revenue by Category</p>
      <div class="flex flex-col gap-2 sm:gap-2.5">
        <div v-for="cat in categoryRevenue" :key="cat.category" class="bar-row">
          <span class="bar-label truncate">{{ cat.category }}</span>
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: cat.percentage + '%', background: chartColor }" />
          </div>
          <span class="bar-val w-16 sm:w-20 text-right">{{ formatCurrency(cat.revenue) }}</span>
        </div>
      </div>
    </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock3, DollarSign, ShoppingBag, Timer } from 'lucide-vue-next'
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatCard from '@/components/ui/StatCard.vue'
import { fetchOwnerOrders, fetchTopItems } from '@/services/owner'

const props = defineProps({
  orders: { type: Array, default: () => [] },
})

const fetchedOrders = ref([])
const topItems = ref([])
const revenueByCategory = ref([])

const tabs = [
  { key: 'today', label: 'Today' },
  { key: 'month', label: 'This month' },
]
const currentTab = ref('today')
const chartColor = 'hsl(var(--primary))'
const sourceOrders = computed(() => (props.orders.length ? props.orders : fetchedOrders.value))

onMounted(() => {
  if (!props.orders.length) {
    loadOrders()
  }
  loadTopItems()
})

// ── helpers ──────────────────────────────────────────────────────────────────

function isToday(date) {
  const d = new Date(date)
  const now = new Date()
  return d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
}

function isThisMonth(date) {
  const d = new Date(date)
  const now = new Date()
  return d.getFullYear() === now.getFullYear() && d.getMonth() === now.getMonth()
}

function isYesterday(date) {
  const d = new Date(date)
  const y = new Date(); y.setDate(y.getDate() - 1)
  return d.getFullYear() === y.getFullYear() &&
    d.getMonth() === y.getMonth() &&
    d.getDate() === y.getDate()
}

function isLastMonth(date) {
  const d = new Date(date)
  const now = new Date()
  const lm = new Date(now.getFullYear(), now.getMonth() - 1, 1)
  return d.getFullYear() === lm.getFullYear() && d.getMonth() === lm.getMonth()
}

function pctDelta(curr, prev) {
  if (prev === 0) return { str: 'N/A', up: true }
  const p = Math.round(((curr - prev) / prev) * 100)
  return { str: (p >= 0 ? '+' : '') + p + '%', up: p >= 0 }
}

async function loadOrders() {
  try {
    fetchedOrders.value = await fetchOwnerOrders()
  } catch {
    fetchedOrders.value = []
  }
}

async function loadTopItems() {
  try {
    const data = await fetchTopItems(10)
    topItems.value = data.top_items || []
    revenueByCategory.value = data.revenue_by_category || []
  } catch {
    topItems.value = []
    revenueByCategory.value = []
  }
}

// ── filtered order sets ───────────────────────────────────────────────────────

const todayOrders    = computed(() => sourceOrders.value.filter(o => isToday(o.created_at)))
const yesterdayOrders = computed(() => sourceOrders.value.filter(o => isYesterday(o.created_at)))
const monthOrders    = computed(() => sourceOrders.value.filter(o => isThisMonth(o.created_at)))
const lastMonthOrders = computed(() => sourceOrders.value.filter(o => isLastMonth(o.created_at)))

const currentOrders  = computed(() => currentTab.value === 'today' ? todayOrders.value : monthOrders.value)
const compareOrders  = computed(() => currentTab.value === 'today' ? yesterdayOrders.value : lastMonthOrders.value)

function totalRevenue(orders) {
  return orders.reduce((s, o) => s + Number(o.total_amount), 0)
}
function avgOrder(orders) {
  return orders.length ? totalRevenue(orders) / orders.length : 0
}
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(Number(value) || 0)
}

// ── metrics ───────────────────────────────────────────────────────────────────

const metrics = computed(() => {
  const curr = currentOrders.value
  const prev = compareOrders.value

  const countDelta   = pctDelta(curr.length, prev.length)
  const revDelta     = pctDelta(totalRevenue(curr), totalRevenue(prev))
  const avgDelta     = pctDelta(avgOrder(curr), avgOrder(prev))

  return [
    { title: 'Orders', value: curr.length.toLocaleString('en-US'), delta: countDelta.str, icon: ShoppingBag },
    { title: 'Revenue', value: formatCurrency(totalRevenue(curr)), delta: revDelta.str, icon: DollarSign },
    { title: 'Avg Order', value: formatCurrency(avgOrder(curr)), delta: avgDelta.str, icon: Clock3 },
    { title: 'Avg Prep Time', value: avgPrepTime.value, delta: prepDelta.value.str, icon: Timer },
  ]
})

function computeAvgPrep(orders) {
  const completed = orders.filter(o => o.status === 'Completed' && o.completed_at)
  if (!completed.length) return null
  const avg = completed.reduce((s, o) => {
    return s + (new Date(o.completed_at) - new Date(o.created_at))
  }, 0) / completed.length
  return Math.round(avg / 60000) // minutes
}

const avgPrepTime = computed(() => {
  const m = computeAvgPrep(currentOrders.value)
  return m !== null ? m + 'm' : '—'
})
const prepDelta = computed(() => {
  const curr = computeAvgPrep(currentOrders.value)
  const prev = computeAvgPrep(compareOrders.value)
  if (curr === null || prev === null) return { str: '—', up: true }
  const diff = curr - prev
  return { str: (diff <= 0 ? '' : '+') + diff + 'm', up: diff <= 0 }
})

// ── revenue chart ─────────────────────────────────────────────────────────────

const chartXLabels = computed(() => {
  if (currentTab.value === 'today') return ['10am','12pm','2pm','4pm','6pm','8pm']
  return ['Wk 1','Wk 2','Wk 3','Wk 4']
})

// Build SVG paths from real revenue data, bucketed by hour or week
const chartPaths = computed(() => {
  const W = 400, H = 120, PAD = 5
  let buckets = []

  if (currentTab.value === 'today') {
    // Hours 10–21 (12 buckets)
    buckets = Array.from({ length: 12 }, (_, i) => {
      const hour = i + 10
      return todayOrders.value
        .filter(o => new Date(o.created_at).getHours() === hour)
        .reduce((s, o) => s + Number(o.total_amount), 0)
    })
  } else {
    // Weeks 1–4 of current month
    buckets = Array.from({ length: 4 }, (_, i) => {
      return monthOrders.value
        .filter(o => {
          const day = new Date(o.created_at).getDate()
          return day >= i * 7 + 1 && day <= (i + 1) * 7
        })
        .reduce((s, o) => s + Number(o.total_amount), 0)
    })
  }

  const max = Math.max(...buckets, 1)
  const n = buckets.length
  const points = buckets.map((v, i) => ({
    x: (i / (n - 1)) * W,
    y: PAD + (1 - v / max) * (H - PAD * 2),
  }))

  // Simple polyline → smooth with cubic bezier
  const lineD = points.reduce((acc, p, i) => {
    if (i === 0) return `M${p.x},${p.y}`
    const prev = points[i - 1]
    const cpx = (prev.x + p.x) / 2
    return acc + ` C${cpx},${prev.y} ${cpx},${p.y} ${p.x},${p.y}`
  }, '')

  const areaD = lineD + ` L${W},${H} L0,${H} Z`

  return { line: lineD, area: areaD }
})

// ── status breakdown ──────────────────────────────────────────────────────────

const STATUS_COLORS = {
  completed: '#639922',
  preparing: '#BA7517',
  ready: '#185FA5',
  cancelled: '#E24B4A',
  new: 'hsl(var(--primary))',
}

const activeStatus = computed(() => {
  const total = currentOrders.value.length || 1
  return Object.entries(STATUS_COLORS)
    .map(([label, color]) => {
      const val = currentOrders.value.filter(o => String(o.status).toLowerCase() === label).length
      return {
        label: label.charAt(0).toUpperCase() + label.slice(1),
        color,
        val,
        pct: Math.round((val / total) * 100),
      }
    })
    .filter(s => s.val > 0)
})

const donutGradient = computed(() => {
  let pos = 0
  const stops = activeStatus.value.map(s => {
    const start = pos; pos += s.pct
    return `${s.color} ${start}% ${pos}%`
  })
  return `conic-gradient(${stops.join(',')})`
})

// ── revenue by category ───────────────────────────────────────────────────────

const categoryRevenue = computed(() => {
  if (!revenueByCategory.value.length) return []
  const total = revenueByCategory.value.reduce((sum, cat) => sum + cat.revenue, 0)
  return revenueByCategory.value.map(cat => ({
    ...cat,
    percentage: total > 0 ? Math.round((cat.revenue / total) * 100) : 0
  }))
})

// ── volume bars ───────────────────────────────────────────────────────────────

const volumeBars = computed(() => {
  if (currentTab.value === 'today') {
    // Mon–Sun of current week
    const now = new Date()
    const day = now.getDay()
    const diff = now.getDate() - day + (day === 0 ? -6 : 1) // Adjust when day is Sunday
    const startOfWeek = new Date(now)
    startOfWeek.setDate(diff)
    startOfWeek.setHours(0, 0, 0, 0)
    
    const days = Array.from({ length: 7 }, (_, i) => {
      const d = new Date(startOfWeek)
      d.setDate(startOfWeek.getDate() + i)
      return d
    })
    
    const counts = days.map(d => {
      return sourceOrders.value.filter(o => {
        const orderDate = new Date(o.created_at)
        // Compare year, month, and day
        return orderDate.getFullYear() === d.getFullYear() &&
               orderDate.getMonth() === d.getMonth() &&
               orderDate.getDate() === d.getDate()
      }).length
    })
    
    const max = Math.max(...counts, 1)
    const labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    return days.map((d, i) => ({ label: labels[i], val: counts[i], max }))
  } else {
    const weeks = Array.from({ length: 4 }, (_, i) => {
      const val = monthOrders.value.filter(o => {
        const day = new Date(o.created_at).getDate()
        return day >= i * 7 + 1 && day <= (i + 1) * 7
      }).length
      return { label: `Wk ${i + 1}`, val }
    })
    const max = Math.max(...weeks.map(w => w.val), 1)
    return weeks.map(w => ({ ...w, max }))
  }
})
</script>

<style scoped>
.card { 
  background: var(--color-background-primary); 
  border: 0.5px solid var(--color-border-tertiary); 
  border-radius: var(--border-radius-lg); 
  padding: 12px;
}
@media (min-width: 640px) {
  .card { padding: 16px; }
}
.label { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-text-tertiary); margin-bottom: 6px; }
.big-num { font-size: 28px; font-weight: 500; color: var(--color-text-primary); line-height: 1; }
.sub { font-size: 12px; color: var(--color-text-tertiary); margin-top: 5px; }
.pill { display: inline-block; font-size: 11px; font-weight: 500; border-radius: 4px; padding: 2px 7px; }
.pill-up { background: #eaf3de; color: #3b6d11; }
.pill-down { background: #fcebeb; color: #a32d2d; }
.section-title { 
  font-size: 12px; 
  font-weight: 500; 
  color: var(--color-text-primary); 
  margin-bottom: 10px; 
}
@media (min-width: 640px) {
  .section-title { font-size: 13px; margin-bottom: 12px; }
}
.bar-row { 
  display: flex; 
  align-items: center; 
  gap: 6px; 
  margin-bottom: 8px; 
}
@media (min-width: 640px) {
  .bar-row { gap: 10px; margin-bottom: 10px; }
}
.bar-label { 
  font-size: 11px; 
  color: var(--color-text-secondary); 
  width: 60px; 
  flex-shrink: 0; 
  text-align: right; 
}
@media (min-width: 640px) {
  .bar-label { font-size: 12px; width: 70px; }
}
.bar-track { flex: 1; height: 8px; background: var(--color-background-secondary); border-radius: 99px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 99px; }
.bar-val { 
  font-size: 11px; 
  color: var(--color-text-tertiary); 
  width: 32px; 
  flex-shrink: 0; 
  text-align: right; 
}
@media (min-width: 640px) {
  .bar-val { font-size: 12px; width: 36px; }
}
.tab-btn { 
  font-size: 11px; 
  font-weight: 500; 
  padding: 3px 10px; 
  border-radius: 6px; 
  border: 0.5px solid transparent; 
  cursor: pointer; 
  transition: all 0.15s; 
  background: none; 
  color: var(--color-text-tertiary); 
}
@media (min-width: 640px) {
  .tab-btn { font-size: 12px; padding: 4px 12px; }
}
.tab-btn.active { background: var(--color-background-primary); border-color: var(--color-border-secondary); color: var(--color-text-primary); }
</style>
