<template>
  <DashboardLayout role="owner">
    <div class="py-4 sm:py-5 space-y-3 sm:space-y-4">

    <!-- Header + tab toggle -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-foreground">Analytics & Insights</h1>
        <p class="text-xs sm:text-sm text-muted-foreground mt-1">Track performance and identify growth opportunities</p>
      </div>
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

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="text-center space-y-3">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto"></div>
        <p class="text-sm text-muted-foreground">Loading analytics...</p>
      </div>
    </div>

    <!-- Analytics Content -->
    <template v-else>
      <!-- Key Insights Cards -->
      <div v-if="insights.length > 0" class="card bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
        <div class="flex items-start gap-2 mb-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <p class="text-sm font-semibold text-foreground">Key Insights</p>
        </div>
        <ul class="space-y-1.5 text-xs sm:text-sm text-foreground/90">
          <li v-for="(insight, idx) in insights" :key="idx" class="flex items-start gap-2">
            <span class="text-primary mt-0.5">•</span>
            <span>{{ insight }}</span>
          </li>
        </ul>
      </div>

      <!-- Primary Metrics -->
      <div class="grid gap-3 sm:gap-4 grid-cols-2 lg:grid-cols-4">
        <StatCard
          v-for="m in metrics"
          :key="m.title"
          :title="m.title"
          :value="m.value"
          :description="m.description"
          :icon="m.icon"
        />
      </div>

      <!-- Performance Indicators -->
      <div class="grid gap-3 sm:gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div class="card">
          <p class="text-xs font-medium text-muted-foreground mb-2">Success Rate</p>
          <p class="text-2xl sm:text-3xl font-bold text-foreground">{{ performanceMetrics.successRate }}%</p>
          <p class="text-xs text-muted-foreground mt-1">Completed orders</p>
          <div class="mt-2 h-2 bg-muted/50 rounded-full overflow-hidden">
            <div class="h-full bg-green-500 rounded-full transition-all" :style="{ width: performanceMetrics.successRate + '%' }"></div>
          </div>
        </div>

        <div class="card">
          <p class="text-xs font-medium text-muted-foreground mb-2">Avg Prep Time</p>
          <p class="text-2xl sm:text-3xl font-bold text-foreground">{{ performanceMetrics.avgPrepTime }}</p>
          <p class="text-xs mt-1" :class="performanceMetrics.prepTrend >= 0 ? 'text-red-600' : 'text-green-600'">
            {{ performanceMetrics.prepTrend >= 0 ? '↑' : '↓' }} {{ Math.abs(performanceMetrics.prepTrend) }}m vs {{ currentTab === 'today' ? 'yesterday' : 'last period' }}
          </p>
        </div>

        <div class="card">
          <p class="text-xs font-medium text-muted-foreground mb-2">Peak Hour</p>
          <p class="text-2xl sm:text-3xl font-bold text-foreground">{{ performanceMetrics.peakHour }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ performanceMetrics.peakOrders }} orders</p>
        </div>

        <div class="card">
          <p class="text-xs font-medium text-muted-foreground mb-2">Growth</p>
          <p class="text-2xl sm:text-3xl font-bold" :class="performanceMetrics.growthRate === null ? 'text-muted-foreground' : performanceMetrics.growthRate >= 0 ? 'text-green-600' : 'text-red-600'">
            {{ performanceMetrics.growthRate === null ? 'New' : `${performanceMetrics.growthRate >= 0 ? '+' : ''}${performanceMetrics.growthRate}%` }}
          </p>
          <p class="text-xs text-muted-foreground mt-1">{{ performanceMetrics.growthRate === null ? 'No baseline yet' : `vs ${currentTab === 'today' ? 'yesterday' : 'last period'}` }}</p>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid gap-3 sm:gap-4 lg:grid-cols-2">
        <!-- Revenue Trend -->
        <div class="card">
          <div class="flex items-center justify-between mb-3">
            <p class="section-title mb-0">Revenue Trend</p>
            <span class="text-xs text-muted-foreground">{{ currentTab === 'today' ? 'By hour' : currentTab === '7days' ? 'Last 7 days' : 'By week' }}</span>
          </div>
          <div class="relative h-32 sm:h-40">
            <svg class="w-full h-[120px] sm:h-[130px]" viewBox="0 0 400 120" preserveAspectRatio="none">
              <defs>
                <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" :stop-color="chartColor" stop-opacity="0.2"/>
                  <stop offset="100%" :stop-color="chartColor" stop-opacity="0"/>
                </linearGradient>
              </defs>
              <line v-for="(y, i) in [0, 40, 80, 119]" :key="i" x1="0" :y1="y" x2="400" :y2="y" stroke="var(--color-border-tertiary)" stroke-width="0.5"/>
              <path :d="chartPaths.area" fill="url(#revenueGradient)"/>
              <path :d="chartPaths.line" fill="none" :stroke="chartColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              <!-- Data points -->
              <circle v-for="(point, i) in chartPoints" :key="i" :cx="point.x" :cy="point.y" r="3" :fill="chartColor" class="drop-shadow-sm"/>
            </svg>
            <div class="flex justify-between mt-1">
              <span v-for="l in chartXLabels" :key="l" class="text-[10px] sm:text-xs text-muted-foreground truncate">{{ l }}</span>
            </div>
          </div>
          <div class="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span>Peak: {{ formatCurrency(Math.max(...revenueData, 0)) }}</span>
            <span>Avg: {{ formatCurrency(revenueData.reduce((a,b) => a+b, 0) / revenueData.length || 0) }}</span>
          </div>
        </div>

        <!-- Order Volume -->
        <div class="card">
          <div class="flex items-center justify-between mb-3">
            <p class="section-title mb-0">Order Volume</p>
            <span class="text-xs text-muted-foreground">{{ currentTab === 'today' ? 'Today by hour' : currentTab === '7days' ? 'Last 7 days' : 'This month' }}</span>
          </div>
          <div class="flex items-end gap-1.5 sm:gap-2 h-24 sm:h-28">
            <div v-for="(b, idx) in volumeBars" :key="b.label" class="flex-1 flex flex-col items-center gap-1 sm:gap-1.5 group cursor-pointer">
              <span class="text-[10px] sm:text-xs font-medium text-foreground group-hover:text-primary transition">{{ b.val }}</span>
              <div class="w-full bg-muted/50 rounded-t-sm sm:rounded-t h-16 sm:h-20 flex items-end overflow-hidden relative">
                <div 
                  :style="{ 
                    height: b.val === 0 ? '2%' : Math.round(b.val / b.max * 100) + '%', 
                    background: idx === volumeHighlightIndex ? 'hsl(var(--primary))' : 'hsl(var(--primary) / 0.6)'
                  }" 
                  class="w-full rounded-t transition-all duration-300 group-hover:brightness-110"
                />
              </div>
              <span class="text-[9px] sm:text-[10px] font-medium truncate w-full text-center" :class="idx === volumeHighlightIndex ? 'text-primary' : 'text-muted-foreground'">
                {{ b.label }}
              </span>
            </div>
          </div>
          <div class="mt-3 text-xs text-muted-foreground text-center">
            Total: {{ volumeBars.reduce((sum, b) => sum + b.val, 0) }} orders • Avg: {{ Math.round(volumeBars.reduce((sum, b) => sum + b.val, 0) / volumeBars.length) }}/day
          </div>
        </div>
      </div>

      <!-- Status & Category Analysis -->
      <div class="grid gap-3 sm:gap-4 lg:grid-cols-2">
        <!-- Order Status Breakdown -->
        <div class="card">
          <p class="section-title">Order Status Distribution</p>
          <div class="space-y-2">
            <div v-for="s in activeStatus" :key="s.label" class="bar-row">
              <span class="bar-label truncate">{{ s.label }}</span>
              <div class="bar-track">
                <div class="bar-fill transition-all duration-500" :style="{ width: s.pct + '%', background: s.color }" />
              </div>
              <span class="bar-val">{{ s.val }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3 sm:gap-4 mt-4 pt-3 border-t border-border">
            <div :style="{ background: donutGradient }" class="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex-shrink-0 shadow-sm" />
            <div class="text-xs sm:text-sm text-muted-foreground leading-relaxed flex-1">
              <div v-for="s in activeStatus" :key="s.label" class="flex items-center justify-between">
                <span><span :style="{ color: s.color }">●</span> {{ s.label }}</span>
                <span class="font-medium">{{ s.pct }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Revenue by Category -->
        <div class="card">
          <p class="section-title">Revenue by Category</p>
          <div v-if="categoryRevenue.length > 0" class="space-y-2 pr-1 sm:pr-2">
            <div v-for="(cat, idx) in categoryRevenue.slice(0, 5)" :key="cat.category" class="bar-row px-1 sm:px-2">
              <span class="bar-label truncate">{{ cat.category }}</span>
              <div class="bar-track">
                <div class="bar-fill transition-all duration-500" :style="{ width: cat.percentage + '%', background: categoryColors[idx % categoryColors.length] }" />
              </div>
              <span class="bar-val w-20 sm:w-24 text-right pr-1">{{ formatCurrency(cat.revenue) }}</span>
            </div>
          </div>
          <p v-else class="text-xs text-muted-foreground text-center py-4">No category data available</p>
          <div v-if="bestCategory" class="mt-4 pt-3 border-t border-border">
            <div class="rounded-xl border border-emerald-200 bg-gradient-to-r from-emerald-50 to-lime-50 px-3 py-2.5 sm:px-4 sm:py-3">
              <div class="flex items-center justify-between gap-3">
                <div class="min-w-0">
                  <p class="text-[10px] sm:text-xs font-semibold uppercase tracking-[0.12em] text-emerald-700">Best Performer</p>
                  <p class="mt-0.5 text-sm sm:text-base font-semibold text-foreground break-words">{{ bestCategory.category }}</p>
                </div>
                <div class="shrink-0 rounded-full bg-emerald-600 px-2 py-1 text-[10px] sm:text-xs font-semibold text-white">
                  {{ bestCategory.percentage }}%
                </div>
              </div>
              <div class="mt-2 flex items-center justify-between text-[11px] sm:text-xs text-muted-foreground">
                <span>Category revenue</span>
                <span class="font-medium text-foreground">{{ formatCurrency(bestCategory.revenue) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Performers -->
      <div class="grid gap-3 sm:gap-4 lg:grid-cols-2">
        <!-- Top Selling Items -->
        <div class="card">
          <div class="flex items-center justify-between mb-3">
            <p class="section-title mb-0">Top Selling Items</p>
            <span class="text-xs font-medium text-primary">🏆 Best Performers</span>
          </div>
          <div v-if="topItems.length > 0" class="space-y-2">
            <div v-for="(item, idx) in topItems.slice(0, 5)" :key="item.id" 
                 class="flex items-center gap-2 sm:gap-3 p-2 sm:p-3 bg-gradient-to-r rounded-lg transition hover:shadow-md"
                 :class="idx === 0 ? 'from-amber-50 to-amber-100/50 border border-amber-200' : 'bg-muted/30'">
              <div class="flex items-center justify-center w-7 h-7 sm:w-8 sm:h-8 rounded-full font-bold text-xs sm:text-sm shrink-0"
                   :class="idx === 0 ? 'bg-amber-500 text-white' : idx === 1 ? 'bg-gray-400 text-white' : idx === 2 ? 'bg-amber-700 text-white' : 'bg-muted text-muted-foreground'">
                {{ idx + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs sm:text-sm font-semibold text-foreground truncate">
                  {{ item.name }}
                </div>
                <div class="text-[10px] sm:text-xs text-muted-foreground">
                  {{ item.total_quantity }} sold • {{ item.category }}
                </div>
              </div>
              <div class="text-right shrink-0">
                <div class="text-sm sm:text-base font-bold text-primary">
                  {{ formatCurrency(item.total_revenue) }}
                </div>
                <div class="text-[10px] text-muted-foreground">
                  {{ formatCurrency(item.total_revenue / item.total_quantity) }}/unit
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-xs text-muted-foreground text-center py-4">No sales data available</p>
        </div>

        <!-- Hourly Performance -->
        <div class="card">
          <p class="section-title">Hourly Performance Heatmap</p>
          <div v-if="hourlyDistribution.length > 0" class="space-y-1.5">
            <div v-for="hour in hourlyDistribution.slice(0, 12)" :key="hour.hour" class="flex items-center gap-2">
              <span class="text-xs font-medium text-muted-foreground w-12 shrink-0">{{ formatHour(hour.hour) }}</span>
              <div class="flex-1 h-6 bg-muted/30 rounded-full overflow-hidden relative">
                <div class="h-full transition-all duration-500 flex items-center px-2"
                     :style="{ 
                       width: (hour.order_count / maxHourlyOrders * 100) + '%',
                       background: getHeatmapColor(hour.order_count, maxHourlyOrders)
                     }">
                  <span v-if="hour.order_count > 0" class="text-[10px] font-medium text-white drop-shadow">
                    {{ hour.order_count }}
                  </span>
                </div>
              </div>
              <span class="text-xs text-muted-foreground w-16 sm:w-20 text-right shrink-0">
                {{ formatCurrency(hour.revenue) }}
              </span>
            </div>
          </div>
          <p v-else class="text-xs text-muted-foreground text-center py-4">No hourly data available</p>
          <div v-if="hourlyDistribution.length > 0" class="mt-4 pt-3 border-t border-border flex items-center justify-between text-xs">
            <span class="text-muted-foreground">Busiest:</span>
            <span class="font-medium text-foreground">{{ formatHour(busiestHour) }} ({{ maxHourlyOrders }} orders)</span>
          </div>
        </div>
      </div>

      <!-- No Data Message -->
      <div v-if="sourceOrders.length === 0" class="card text-center py-8">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <p class="text-sm font-medium text-foreground mb-1">No Analytics Data Available</p>
        <p class="text-xs text-muted-foreground">Create some orders to see insights and performance metrics</p>
      </div>
    </template>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { h, ref, computed, onMounted, watch } from 'vue'
import { Clock3, DollarSign, ShoppingBag, Timer, TrendingUp } from 'lucide-vue-next'
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatCard from '@/components/ui/StatCard.vue'
import { fetchOwnerOrders, fetchDailySales } from '@/services/owner'

const props = defineProps({
  orders: { type: Array, default: () => [] },
})

const loading = ref(false)
const fetchedOrders = ref([])
const dailySalesData = ref([])

const tabs = [
  { key: 'today', label: 'Today' },
  { key: '7days', label: '7 Days' },
  { key: 'month', label: 'This Month' },
]

const BahtIcon = {
  render() {
    return h('span', { class: 'text-lg font-bold leading-none' }, '฿')
  },
}

const currentTab = ref('today')
const chartColor = 'hsl(var(--primary))'
const categoryColors = ['#639922', '#BA7517', '#185FA5', '#E24B4A', '#8B5CF6']

const sourceOrders = computed(() => (props.orders.length ? props.orders : fetchedOrders.value))

onMounted(async () => {
  loading.value = true
  try {
    if (!props.orders.length) {
      await loadOrders()
    }
    await loadDailySales(7)
  } finally {
    loading.value = false
  }
})

watch(currentTab, () => {
  // Reload data when tab changes if needed
  if (currentTab.value === '7days') {
    loadDailySales(7)
  }
})

// ── Data Loading ──────────────────────────────────────────────────────────────

async function loadOrders() {
  try {
    fetchedOrders.value = await fetchOwnerOrders()
  } catch {
    fetchedOrders.value = []
  }
}

async function loadDailySales(days = 7) {
  try {
    const data = await fetchDailySales(days)
    dailySalesData.value = data.daily_sales || []
  } catch {
    dailySalesData.value = []
  }
}

// ── Date Helpers ──────────────────────────────────────────────────────────────

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

function isLast7Days(date) {
  const d = new Date(date)
  const now = new Date()
  const startOfToday = new Date(now)
  startOfToday.setHours(0, 0, 0, 0)
  const start = new Date(startOfToday)
  start.setDate(start.getDate() - 6)
  return d >= start && d <= now
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
  if (prev === 0) return { str: 'N/A', up: true, val: 0 }
  if (curr === 0) return { str: '0%', up: true, val: 0 }
  const p = Math.round(((curr - prev) / prev) * 100)
  return { str: (p >= 0 ? '+' : '') + p + '%', up: p >= 0, val: p }
}

// ── Filtered Orders ───────────────────────────────────────────────────────────

const todayOrders    = computed(() => sourceOrders.value.filter(o => isToday(o.created_at)))
const yesterdayOrders = computed(() => sourceOrders.value.filter(o => isYesterday(o.created_at)))
const last7DaysOrders = computed(() => sourceOrders.value.filter(o => isLast7Days(o.created_at)))
const monthOrders    = computed(() => sourceOrders.value.filter(o => isThisMonth(o.created_at)))
const lastMonthOrders = computed(() => sourceOrders.value.filter(o => isLastMonth(o.created_at)))

const currentOrders  = computed(() => {
  if (currentTab.value === 'today') return todayOrders.value
  if (currentTab.value === '7days') return last7DaysOrders.value
  return monthOrders.value
})

const compareOrders  = computed(() => {
  if (currentTab.value === 'today') return yesterdayOrders.value
  if (currentTab.value === '7days') {
    // Compare to previous 7 days
    const now = new Date()
    const fourteenDaysAgo = new Date(now)
    fourteenDaysAgo.setDate(now.getDate() - 14)
    const sevenDaysAgo = new Date(now)
    sevenDaysAgo.setDate(now.getDate() - 7)
    return sourceOrders.value.filter(o => {
      const d = new Date(o.created_at)
      return d >= fourteenDaysAgo && d < sevenDaysAgo
    })
  }
  return lastMonthOrders.value
})

// ── Calculations ──────────────────────────────────────────────────────────────

function totalRevenue(orders) {
  return orders.filter(o => String(o.payment_status).toLowerCase() === 'paid')
    .reduce((s, o) => s + Number(o.total_amount), 0)
}

function avgOrder(orders) {
  const paidOrders = orders.filter(o => String(o.payment_status).toLowerCase() === 'paid')
  return paidOrders.length ? totalRevenue(orders) / paidOrders.length : 0
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(Number(value) || 0)
}

function formatCurrencyCompact(value) {
  const numeric = Number(value) || 0
  if (Math.abs(numeric) < 1000) {
    return formatCurrency(numeric)
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(numeric)
}

function formatCurrencyTwoLine(value) {
  const formatted = formatCurrencyCompact(value)
  const amount = formatted.replace(/^THB\s*/, '')
  return `${amount}`
}

function formatDeltaDescription(delta, context) {
  if (delta.str === 'N/A') {
    return context === 'per-order' ? 'No baseline per order' : 'No baseline yet'
  }

  if (delta.val === 0) {
    return context === 'per-order' ? 'No change per order' : `No change vs ${context}`
  }

  return context === 'per-order' ? `${delta.str} per order` : `${delta.str} vs ${context}`
}

function isSameDay(a, b) {
  return a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
}

// ── Key Insights ──────────────────────────────────────────────────────────────

const insights = computed(() => {
  const results = []
  const curr = currentOrders.value
  
  if (curr.length === 0) return results

  // Revenue growth insight
  const revDelta = pctDelta(totalRevenue(curr), totalRevenue(compareOrders.value))
  if (Math.abs(revDelta.val) > 10) {
    results.push(`Revenue ${revDelta.val >= 0 ? 'increased' : 'decreased'} by ${Math.abs(revDelta.val)}% compared to ${currentTab.value === 'today' ? 'yesterday' : 'previous period'}`)
  }

  // Best selling item
  if (topItems.value.length > 0) {
    results.push(`"${topItems.value[0].name}" is your top seller with ${topItems.value[0].total_quantity} orders`)
  }

  // Peak hour recommendation
  if (hourlyDistribution.value.length > 0) {
    const peak = hourlyDistribution.value.reduce((max, h) => h.order_count > max.order_count ? h : max, hourlyDistribution.value[0])
    results.push(`Peak business hours are around ${formatHour(peak.hour)} - consider staffing accordingly`)
  }

  // Category performance
  if (revenueByCategory.value.length > 1) {
    const topCat = revenueByCategory.value[0]
    const totalCatRevenue = revenueByCategory.value.reduce((sum, c) => sum + c.revenue, 0)
    const pct = Math.round((topCat.revenue / totalCatRevenue) * 100)
    if (pct > 40) {
      results.push(`${topCat.category} dominates with ${pct}% of revenue - consider expanding this category`)
    }
  }

  // Success rate insight
  const completed = curr.filter(o => String(o.status).toLowerCase() === 'completed').length
  const successRate = Math.round((completed / curr.length) * 100)
  if (successRate < 80) {
    results.push(`${100 - successRate}% of orders are incomplete - review operational efficiency`)
  }

  return results.slice(0, 3) // Show max 3 insights
})

// ── Primary Metrics ───────────────────────────────────────────────────────────

const metrics = computed(() => {
  const curr = currentOrders.value
  const prev = compareOrders.value
  const compareLabel = currentTab.value === 'today' ? 'yesterday' : 'previous period'

  const countDelta   = pctDelta(curr.length, prev.length)
  const revDelta     = pctDelta(totalRevenue(curr), totalRevenue(prev))
  const avgDelta     = pctDelta(avgOrder(curr), avgOrder(prev))

  return [
    { 
      title: 'Orders', 
      value: curr.length.toLocaleString('en-US'), 
      description: formatDeltaDescription(countDelta, compareLabel),
      icon: ShoppingBag 
    },
    { 
      title: 'Revenue', 
      value: formatCurrencyTwoLine(totalRevenue(curr)),
      description: formatDeltaDescription(revDelta, compareLabel),
      icon: BahtIcon 
    },
    { 
      title: 'Avg Order', 
      value: formatCurrencyTwoLine(avgOrder(curr)),
      description: formatDeltaDescription(avgDelta, 'per-order'),
      icon: TrendingUp 
    },
    { 
      title: 'Avg Prep Time', 
      value: avgPrepTime.value, 
      description: prepDelta.value.str + ' vs previous',
      icon: Timer 
    },
  ]
})

function computeAvgPrep(orders) {
  const completed = orders.filter(
    (o) => String(o.status).toLowerCase() === 'completed' && o.closed_at
  )
  if (!completed.length) return null
  const avg = completed.reduce((s, o) => {
    return s + (new Date(o.closed_at) - new Date(o.created_at))
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

// ── Performance Metrics ───────────────────────────────────────────────────────

const performanceMetrics = computed(() => {
  const curr = currentOrders.value
  const prev = compareOrders.value
  
  // Success rate (completed orders)
  const completed = curr.filter(o => String(o.status).toLowerCase() === 'completed').length
  const successRate = curr.length > 0 ? Math.round((completed / curr.length) * 100) : 0

  // Prep time
  const currentPrep = computeAvgPrep(curr) || 0
  const prevPrep = computeAvgPrep(prev) || 0
  const prepTrend = currentPrep - prevPrep

  // Peak hour
  let peakHour = '—'
  let peakOrders = 0
  if (hourlyDistribution.value.length > 0) {
    const peak = hourlyDistribution.value.reduce((max, h) => h.order_count > max.order_count ? h : max, hourlyDistribution.value[0])
    peakHour = formatHour(peak.hour)
    peakOrders = peak.order_count
  }

  // Growth rate
  const currRev = totalRevenue(curr)
  const prevRev = totalRevenue(prev)
  const growthRate = prevRev > 0
    ? (currRev <= 0 ? 0 : Math.round(((currRev - prevRev) / prevRev) * 100))
    : null

  return {
    successRate,
    avgPrepTime: avgPrepTime.value,
    prepTrend,
    peakHour,
    peakOrders,
    growthRate
  }
})

const currentPaidOrders = computed(() =>
  currentOrders.value.filter((o) => String(o.payment_status).toLowerCase() === 'paid')
)

const topItems = computed(() => {
  const itemMap = new Map()

  currentPaidOrders.value.forEach((order) => {
    ;(order.items || []).forEach((item) => {
      const key = String(item.menu_item_id ?? `deleted-${item.id}`)
      const quantity = Number(item.quantity) || 0
      const totalRevenue = (Number(item.unit_price) || 0) * quantity
      const existing = itemMap.get(key)

      if (existing) {
        existing.total_quantity += quantity
        existing.total_revenue += totalRevenue
        existing.order_ids.add(order.id)
        return
      }

      itemMap.set(key, {
        id: item.menu_item_id ?? `deleted-${item.id}`,
        name: item.menu_item?.name || 'Deleted item',
        category: item.menu_item?.category || 'Uncategorized',
        price: Number(item.unit_price) || 0,
        total_quantity: quantity,
        total_revenue: totalRevenue,
        order_ids: new Set([order.id]),
      })
    })
  })

  return Array.from(itemMap.values())
    .map((entry) => ({
      ...entry,
      order_count: entry.order_ids.size,
    }))
    .sort((a, b) => b.total_quantity - a.total_quantity)
})

const revenueByCategory = computed(() => {
  const categoryMap = new Map()

  topItems.value.forEach((item) => {
    const key = item.category || 'Uncategorized'
    const existing = categoryMap.get(key)
    if (existing) {
      existing.revenue += item.total_revenue
      existing.quantity += item.total_quantity
      return
    }

    categoryMap.set(key, {
      category: key,
      revenue: item.total_revenue,
      quantity: item.total_quantity,
    })
  })

  return Array.from(categoryMap.values()).sort((a, b) => b.revenue - a.revenue)
})

const hourlyDistribution = computed(() => {
  const buckets = Array.from({ length: 24 }, (_, hour) => ({
    hour,
    order_count: 0,
    revenue: 0,
  }))

  currentPaidOrders.value.forEach((order) => {
    const hour = new Date(order.created_at).getHours()
    const bucket = buckets[hour]
    if (!bucket) return

    bucket.order_count += 1
    bucket.revenue += (order.items || []).reduce(
      (sum, item) => sum + (Number(item.unit_price) || 0) * (Number(item.quantity) || 0),
      0
    )
  })

  return buckets.filter((bucket) => bucket.order_count > 0)
})

// ── Chart Data ────────────────────────────────────────────────────────────────

const revenueData = computed(() => {
  if (currentTab.value === '7days' && dailySalesData.value.length > 0) {
    return dailySalesData.value.slice().reverse().map(d => d.revenue)
  }

  if (currentTab.value === 'today') {
    // Hours 10–21 (12 buckets)
    return Array.from({ length: 12 }, (_, i) => {
      const hour = i + 10
      return todayOrders.value
        .filter(o => new Date(o.created_at).getHours() === hour)
        .reduce((s, o) => s + (String(o.payment_status).toLowerCase() === 'paid' ? Number(o.total_amount) : 0), 0)
    })
  } else {
    // Weeks 1–4 of current month
    return Array.from({ length: 4 }, (_, i) => {
      return monthOrders.value
        .filter(o => {
          const day = new Date(o.created_at).getDate()
          return day >= i * 7 + 1 && day <= (i + 1) * 7
        })
        .reduce((s, o) => s + (String(o.payment_status).toLowerCase() === 'paid' ? Number(o.total_amount) : 0), 0)
    })
  }
})

const chartXLabels = computed(() => {
  if (currentTab.value === '7days' && dailySalesData.value.length > 0) {
    return dailySalesData.value.slice().reverse().map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
  }
  if (currentTab.value === 'today') return ['10am','12pm','2pm','4pm','6pm','8pm','10pm']
  return ['Wk 1','Wk 2','Wk 3','Wk 4']
})

const chartPoints = computed(() => {
  const W = 400, H = 120, PAD = 5
  const buckets = revenueData.value
  const max = Math.max(...buckets, 1)
  const n = buckets.length
  
  return buckets.map((v, i) => ({
    x: (i / Math.max(n - 1, 1)) * W,
    y: PAD + (1 - v / max) * (H - PAD * 2),
  }))
})

const chartPaths = computed(() => {
  const W = 400, H = 120
  const points = chartPoints.value

  if (points.length === 0) {
    return { line: '', area: '' }
  }

  // Smooth line using cubic bezier
  const lineD = points.reduce((acc, p, i) => {
    if (i === 0) return `M${p.x},${p.y}`
    const prev = points[i - 1]
    const cpx = (prev.x + p.x) / 2
    return acc + ` C${cpx},${prev.y} ${cpx},${p.y} ${p.x},${p.y}`
  }, '')

  const areaD = lineD + ` L${W},${H} L0,${H} Z`

  return { line: lineD, area: areaD }
})

// ── Status Breakdown ──────────────────────────────────────────────────────────

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

// ── Category Revenue ──────────────────────────────────────────────────────────

const categoryRevenue = computed(() => {
  if (!revenueByCategory.value.length) return []
  const total = revenueByCategory.value.reduce((sum, cat) => sum + cat.revenue, 0)
  return revenueByCategory.value.map(cat => ({
    ...cat,
    percentage: total > 0 ? Math.round((cat.revenue / total) * 100) : 0
  }))
})

const bestCategory = computed(() => categoryRevenue.value[0] || null)

// ── Volume Bars ───────────────────────────────────────────────────────────────

const volumeBars = computed(() => {
  if (currentTab.value === 'today') {
    // Today by service hours
    const hours = [10, 12, 14, 16, 18, 20, 22]
    const counts = hours.map((hour) =>
      todayOrders.value.filter((o) => new Date(o.created_at).getHours() === hour).length
    )
    const max = Math.max(...counts, 1)
    const labels = ['10a', '12p', '2p', '4p', '6p', '8p', '10p']
    return labels.map((label, i) => ({ label, val: counts[i], max }))
  }

  if (currentTab.value === '7days') {
    // Last 7 calendar days ending today
    const now = new Date()
    const today = new Date(now)
    today.setHours(0, 0, 0, 0)
    const start = new Date(today)
    start.setDate(start.getDate() - 6)

    const days = Array.from({ length: 7 }, (_, i) => {
      const d = new Date(start)
      d.setDate(start.getDate() + i)
      return d
    })

    const counts = days.map((d) => {
      return sourceOrders.value.filter((o) => {
        const orderDate = new Date(o.created_at)
        return isSameDay(orderDate, d)
      }).length
    })

    const max = Math.max(...counts, 1)
    const labels = days.map((d) =>
      d.toLocaleDateString('en-US', { weekday: 'short' })
    )
    return days.map((d, i) => ({ label: labels[i], val: counts[i], max, date: d }))
  } else {
    // Weeks of month
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

const volumeHighlightIndex = computed(() => {
  if (currentTab.value === 'today') {
    const currentHour = new Date().getHours()
    const hours = [10, 12, 14, 16, 18, 20, 22]
    const idx = hours.findIndex((h) => currentHour <= h)
    return idx === -1 ? hours.length - 1 : idx
  }

  if (currentTab.value === '7days') {
    return volumeBars.value.length - 1
  }

  const dayOfMonth = new Date().getDate()
  return Math.min(3, Math.floor((dayOfMonth - 1) / 7))
})

// ── Hourly Distribution ───────────────────────────────────────────────────────

const maxHourlyOrders = computed(() => {
  if (hourlyDistribution.value.length === 0) return 1
  return Math.max(...hourlyDistribution.value.map(h => h.order_count), 1)
})

const busiestHour = computed(() => {
  if (hourlyDistribution.value.length === 0) return 12
  return hourlyDistribution.value.reduce((max, h) => h.order_count > max.order_count ? h : max, hourlyDistribution.value[0]).hour
})

function formatHour(hour) {
  const h = Number(hour)
  if (h === 0) return '12am'
  if (h === 12) return '12pm'
  if (h < 12) return `${h}am`
  return `${h - 12}pm`
}

function getHeatmapColor(count, max) {
  const intensity = count / max
  if (intensity > 0.8) return 'linear-gradient(90deg, #dc2626, #ef4444)'
  if (intensity > 0.6) return 'linear-gradient(90deg, #ea580c, #f97316)'
  if (intensity > 0.4) return 'linear-gradient(90deg, #d97706, #f59e0b)'
  if (intensity > 0.2) return 'linear-gradient(90deg, #16a34a, #22c55e)'
  return 'hsl(var(--primary) / 0.3)'
}
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
