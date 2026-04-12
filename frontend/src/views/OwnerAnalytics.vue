<template>
  <DashboardLayout role="owner">
    <div style="padding: 20px 0;">

    <!-- Header + tab toggle -->
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px;">
      <p style="font-size:15px; font-weight:500; color:var(--color-text-primary);">Overview</p>
      <div style="display:flex; gap:4px; background:var(--color-background-secondary); padding:3px; border-radius:8px; border:0.5px solid var(--color-border-tertiary);">
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
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4" style="margin-bottom:12px;">
      <StatCard
        v-for="m in metrics"
        :key="m.title"
        :title="m.title"
        :value="m.value"
        :description="`${m.delta} vs ${currentTab === 'today' ? 'yesterday' : 'last month'}`"
        :icon="m.icon"
      />
    </div>

    <div class="grid-2" style="margin-bottom:12px;">
      <!-- Revenue chart -->
      <div class="card">
        <p class="section-title">{{ currentTab === 'today' ? 'Revenue by hour' : 'Revenue by week' }}</p>
        <div style="position:relative; height:150px;">
          <svg style="width:100%; height:130px;" viewBox="0 0 400 120" preserveAspectRatio="none">
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
          <div style="display:flex; justify-content:space-between; margin-top:2px;">
            <span v-for="l in chartXLabels" :key="l" style="font-size:11px; color:var(--color-text-tertiary);">{{ l }}</span>
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
        <div style="display:flex; align-items:center; gap:14px; margin-top:10px; flex-wrap:wrap;">
          <div :style="{ background: donutGradient }" style="width:52px; height:52px; border-radius:50%; flex-shrink:0;" />
          <div style="font-size:12px; color:var(--color-text-secondary); line-height:2;">
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
      <p v-if="sourceOrders.length === 0" style="font-size:12px; color:var(--color-text-tertiary); margin-bottom:8px;">
        No orders found. Create some orders to see data.
      </p>
      <div style="display:flex; align-items:flex-end; gap:6px; height:100px;">
        <div v-for="b in volumeBars" :key="b.label" style="flex:1; display:flex; flex-direction:column; align-items:center; gap:4px;">
          <span style="font-size:11px; color:var(--color-text-tertiary);">{{ b.val }}</span>
          <div style="width:100%; background:var(--color-background-secondary); border-radius:4px; height:72px; display:flex; align-items:flex-end; overflow:hidden;">
            <div :style="{ height: b.val === 0 ? '2%' : Math.round(b.val / b.max * 100) + '%', background: b.val === 0 ? 'var(--color-border-tertiary)' : chartColor }" style="width:100%; border-radius:4px 4px 0 0; opacity:0.85;" />
          </div>
          <span style="font-size:11px; color:var(--color-text-tertiary);">{{ b.label }}</span>
        </div>
      </div>
    </div>

    <!-- Top Selling Items -->
    <div class="card" v-if="topItems.length">
      <p class="section-title">Top Selling Items</p>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div v-for="(item, idx) in topItems.slice(0, 5)" :key="item.id" 
             style="display: flex; align-items: center; gap: 10px; padding: 8px; background: var(--color-background-secondary); border-radius: 8px;">
          <span style="font-size:14px; font-weight:600; color:var(--color-text-tertiary); width:24px; text-align:center;">
            {{ idx + 1 }}
          </span>
          <div style="flex: 1;">
            <div style="font-size:13px; font-weight:500; color:var(--color-text-primary);">
              {{ item.name }}
            </div>
            <div style="font-size:11px; color:var(--color-text-tertiary);">
              {{ item.total_quantity }} sold • {{ item.category }}
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size:14px; font-weight:600; color:var(--primary);">
              ฿{{ item.total_revenue.toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Revenue by Category -->
    <div class="card" v-if="categoryRevenue.length">
      <p class="section-title">Revenue by Category</p>
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <div v-for="cat in categoryRevenue" :key="cat.category" class="bar-row">
          <span class="bar-label">{{ cat.category }}</span>
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: cat.percentage + '%', background: chartColor }" />
          </div>
          <span class="bar-val" style="width: 80px;">฿{{ cat.revenue.toFixed(2) }}</span>
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

// ── metrics ───────────────────────────────────────────────────────────────────

const metrics = computed(() => {
  const curr = currentOrders.value
  const prev = compareOrders.value

  const countDelta   = pctDelta(curr.length, prev.length)
  const revDelta     = pctDelta(totalRevenue(curr), totalRevenue(prev))
  const avgDelta     = pctDelta(avgOrder(curr), avgOrder(prev))

  return [
    { title: 'Orders', value: curr.length.toLocaleString(), delta: countDelta.str, icon: ShoppingBag },
    { title: 'Revenue', value: '฿' + totalRevenue(curr).toFixed(2), delta: revDelta.str, icon: DollarSign },
    { title: 'Avg Order', value: '฿' + avgOrder(curr).toFixed(2), delta: avgDelta.str, icon: Clock3 },
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
.grid-4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
.grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); padding: 16px; }
.label { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-text-tertiary); margin-bottom: 6px; }
.big-num { font-size: 28px; font-weight: 500; color: var(--color-text-primary); line-height: 1; }
.sub { font-size: 12px; color: var(--color-text-tertiary); margin-top: 5px; }
.pill { display: inline-block; font-size: 11px; font-weight: 500; border-radius: 4px; padding: 2px 7px; }
.pill-up { background: #eaf3de; color: #3b6d11; }
.pill-down { background: #fcebeb; color: #a32d2d; }
.section-title { font-size: 13px; font-weight: 500; color: var(--color-text-primary); margin-bottom: 12px; }
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.bar-label { font-size: 12px; color: var(--color-text-secondary); width: 70px; flex-shrink: 0; text-align: right; }
.bar-track { flex: 1; height: 8px; background: var(--color-background-secondary); border-radius: 99px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 99px; }
.bar-val { font-size: 12px; color: var(--color-text-tertiary); width: 36px; flex-shrink: 0; text-align: right; }
.tab-btn { font-size: 12px; font-weight: 500; padding: 4px 12px; border-radius: 6px; border: 0.5px solid transparent; cursor: pointer; transition: all 0.15s; background: none; color: var(--color-text-tertiary); }
.tab-btn.active { background: var(--color-background-primary); border-color: var(--color-border-secondary); color: var(--color-text-primary); }
</style>
