<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div>
        <h1 class="font-heading text-3xl font-bold text-foreground">Dashboard</h1>
        <p class="mt-1 text-sm text-muted-foreground">Overview of today's operations</p>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          v-for="stat in stats"
          :key="stat.title"
          :title="stat.title"
          :value="stat.value"
          :icon="stat.icon"
          :description="stat.description"
        />
      </div>

      <div class="grid gap-4 xl:grid-cols-2">
        <PanelCard title="Recent Orders" subtitle="Live kitchen and floor activity">
          <div class="space-y-3">
            <div
              v-for="order in recentOrders"
              :key="order.id"
              class="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3"
            >
              <div>
                <p class="text-sm font-semibold text-foreground">Table {{ order.table_number }}</p>
                <p class="mt-1 text-xs text-muted-foreground">{{ order.items.length }} items</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-foreground">${{ order.total_amount.toFixed(2) }}</p>
                <div class="mt-2">
                  <StatusBadge :status="order.status" />
                </div>
              </div>
            </div>
          </div>
        </PanelCard>

        <PanelCard title="Popular Items" subtitle="Top menu items for today">
          <div class="space-y-3">
            <div
              v-for="(item, index) in popularItems"
              :key="item.id"
              class="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3"
            >
              <div class="flex items-center gap-4">
                <span class="font-heading text-2xl font-bold text-muted-foreground">#{{ index + 1 }}</span>
                <div>
                  <p class="text-sm font-semibold text-foreground">{{ item.name }}</p>
                  <p class="mt-1 text-xs text-muted-foreground">{{ item.category }}</p>
                </div>
              </div>
              <p class="text-sm font-semibold text-foreground">${{ item.price.toFixed(2) }}</p>
            </div>
          </div>
        </PanelCard>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed } from 'vue'
import { DollarSign, ShoppingBag, Clock, TrendingUp } from 'lucide-vue-next'

import DashboardLayout from '@/components/DashboardLayout.vue'
import PanelCard from '@/components/ui/PanelCard.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { mockOrders, mockMenuItems } from '@/data/mock-data'

const stats = [
  {
    title: 'Total Revenue',
    value: `$${mockOrders.reduce((s, o) => s + o.total_amount, 0).toFixed(2)}`,
    icon: DollarSign,
    description: "Today's earnings",
  },
  {
    title: 'Active Orders',
    value: mockOrders.filter(o => !['Completed', 'Cancelled'].includes(o.status)).length,
    icon: Clock,
    description: 'Currently in progress',
  },
  {
    title: 'Total Orders',
    value: mockOrders.length,
    icon: ShoppingBag,
    description: 'Orders today',
  },
  {
    title: 'Menu Items',
    value: mockMenuItems.filter(i => i.is_available).length,
    icon: TrendingUp,
    description: 'Items available',
  },
]

const recentOrders = computed(() => mockOrders.slice(0, 5))
const popularItems = computed(() => mockMenuItems.slice(0, 5))
</script>
