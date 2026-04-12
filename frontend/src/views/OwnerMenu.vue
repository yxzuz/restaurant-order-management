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

      <p
        v-if="errorMessage"
        class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ errorMessage }}
      </p>

      <p v-if="loading" class="text-sm text-muted-foreground">Loading menu items...</p>

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
import { onMounted, ref } from 'vue'

import DashboardLayout from '@/components/DashboardLayout.vue'
import OwnerEditModal from '@/components/OwnerEditModal.vue'
import OwnerMenuItemCard from '@/components/OwnerMenuItemCard.vue'
import {
  createMenuItem,
  deleteMenuItem as deleteMenuItemRequest,
  fetchOwnerMenuItems,
  updateMenuItem,
} from '@/services/owner'

const menuItems = ref([])
const selectedItem = ref(null)
const showEditModal = ref(false)
const loading = ref(false)
const errorMessage = ref('')

onMounted(() => {
  loadMenuItems()
})

async function loadMenuItems() {
  loading.value = true
  errorMessage.value = ''

  try {
    menuItems.value = await fetchOwnerMenuItems()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not load menu items.'
  } finally {
    loading.value = false
  }
}

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

async function saveItem(updatedItem) {
  errorMessage.value = ''

  try {
    if (selectedItem.value) {
      const savedItem = await updateMenuItem(updatedItem.id, updatedItem)
      menuItems.value = menuItems.value.map((item) =>
        item.id === savedItem.id ? { ...item, ...savedItem } : item
      )
    } else {
      const savedItem = await createMenuItem(updatedItem)
      menuItems.value = [...menuItems.value, savedItem]
    }

    closeEditModal()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not save menu item.'
  }
}

async function deleteItem(item) {
  errorMessage.value = ''

  try {
    await deleteMenuItemRequest(item.id)
    menuItems.value = menuItems.value.filter((menuItem) => menuItem.id !== item.id)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not delete menu item.'
  }
}

async function toggleAvailability(item) {
  errorMessage.value = ''

  try {
    const savedItem = await updateMenuItem(item.id, {
      ...item,
      is_available: !item.is_available,
    })

    menuItems.value = menuItems.value.map((menuItem) =>
      menuItem.id === savedItem.id ? { ...menuItem, ...savedItem } : menuItem
    )
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not update availability.'
  }
}
</script>
