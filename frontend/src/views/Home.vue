<template>
  <div class="min-h-screen bg-background">

    <!-- HERO -->
    <section class="relative h-[50vh] min-h-[360px] overflow-hidden">
      <img
        src="@/assets/hero-restaurant.jpg"
        class="absolute inset-0 w-full h-full object-cover"
      />

      <div class="absolute inset-0 bg-black/60"></div>

      <div class="relative z-10 h-full flex flex-col items-center justify-center text-center px-4">
        <div class="flex items-center gap-2 mb-4">
          <UtensilsCrossed class="h-8 w-8 text-orange-400" />
          <h1 class="text-4xl md:text-5xl font-bold text-white">
            OrderFlow
          </h1>
        </div>

        <p class="text-gray-200 text-lg max-w-md">
          Digital restaurant order tracking — fast, accurate, and effortless.
        </p>
      </div>
    </section>

    <!-- ROLES -->
    <section class="max-w-4xl mx-auto -mt-16 relative z-20 pb-16 px-4">
      <div class="grid gap-4 md:grid-cols-3">

        <router-link
          v-for="role in roles"
          :key="role.title"
          :to="role.link"
        >
          <div class="bg-white rounded-2xl p-6 shadow-lg hover:-translate-y-1 hover:shadow-xl transition cursor-pointer text-center">

            <component :is="role.icon" :class="['h-10 w-10 mx-auto mb-2', role.iconClass]" />

            <h3 class="text-xl font-semibold">
              {{ role.title }}
            </h3>

            <p class="text-gray-600 mt-2">
              {{ role.description }}
            </p>

          </div>
        </router-link>

      </div>

      <p class="mt-10 text-center text-sm text-gray-500">
        Demo mode — click any role above to explore the platform.
      </p>
    </section>

  </div>
</template>

<script setup>
import { UtensilsCrossed, ClipboardList, BarChart3, QrCode } from 'lucide-vue-next'

const roles = [
  {
    title: 'Customer',
    description: 'Browse the menu and place orders from your table',
    icon: QrCode,
    iconClass: 'text-orange-600',
    link: '/table/5?token=qr-token-5',
  },
  {
    title: 'Staff',
    description: 'View and manage incoming orders in real-time',
    icon: ClipboardList,
    iconClass: 'text-blue-600',
    link: '/staff/orders',
  },
  {
    title: 'Owner',
    description: 'Manage menu, staff, and view analytics',
    icon: BarChart3,
    iconClass: 'text-green-600',
    link: '/owner/dashboard',
  },
]
</script>