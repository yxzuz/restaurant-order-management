<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="font-heading text-3xl font-bold text-foreground">Menu Management</h1>
          <p class="mt-1 text-sm text-muted-foreground">Add, edit, or remove menu items</p>
        </div>

        <button class="rounded-lg bg-primary px-4 py-2 text-white" @click="openCreate">
          + Add Item
        </button>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <OwnerMenuItemCard
          v-for="item in menuItems"
          :key="item.id"
          :item="item"
          @edit="openEdit"
          @delete="deleteItem"
          @toggle-availability="toggleAvailability"
        />
      </div>
    </div>

    <OwnerEditModal
      v-if="showEditModal"
      :item="selectedItem"
      @close="closeEditModal"
      @save="saveItem"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'

import DashboardLayout from '@/components/DashboardLayout.vue'
import OwnerEditModal from '@/components/OwnerEditModal.vue'
import OwnerMenuItemCard from '@/components/OwnerMenuItemCard.vue'
import { mockMenuItems } from '@/data/mock-data'

const menuItems = ref(mockMenuItems.map((item) => ({ ...item })))
const selectedItem = ref(null)
const showEditModal = ref(false)

function openCreate() {
  selectedItem.value = null
  showEditModal.value = true
}

function openEdit(item) {
  selectedItem.value = { ...item }
  showEditModal.value = true
}

function closeEditModal() {
  selectedItem.value = null
  showEditModal.value = false
}

function saveItem(updatedItem) {
  if (selectedItem.value) {
    menuItems.value = menuItems.value.map((item) =>
      item.id === updatedItem.id ? { ...item, ...updatedItem } : item
    )
  } else {
    menuItems.value = [
      ...menuItems.value,
      {
        ...updatedItem,
        id: Date.now(),
      },
    ]
  }

  closeEditModal()
}

function deleteItem(item) {
  menuItems.value = menuItems.value.filter((menuItem) => menuItem.id !== item.id)
}

function toggleAvailability(item) {
  menuItems.value = menuItems.value.map((menuItem) =>
    menuItem.id === item.id
      ? { ...menuItem, is_available: !menuItem.is_available }
      : menuItem
  )
}
</script>
