<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div>
        <h1 class="font-heading text-3xl font-bold text-foreground">Staff Accounts</h1>
        <p class="mt-1 text-sm text-muted-foreground">Create and review staff login access</p>
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

      <div class="grid gap-4 xl:grid-cols-[380px_minmax(0,1fr)]">
        <section class="rounded-2xl border border-border bg-card p-5 shadow-sm">
          <h2 class="font-heading text-xl font-bold text-foreground">Add Staff Account</h2>
          <form class="mt-4 space-y-4" @submit.prevent="submitStaff">
            <div>
              <label class="mb-1 block text-sm font-medium text-foreground">Username</label>
              <input
                v-model="form.username"
                type="text"
                class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
              >
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium text-foreground">Password</label>
              <input
                v-model="form.password"
                type="password"
                class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
              >
            </div>

            <button
              type="submit"
              class="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90 disabled:opacity-60"
              :disabled="submitting"
            >
              {{ submitting ? 'Creating...' : 'Create Staff' }}
            </button>
          </form>
        </section>

        <section class="rounded-2xl border border-border bg-card p-5 shadow-sm">
          <div class="flex items-center justify-between gap-3">
            <div>
              <h2 class="font-heading text-xl font-bold text-foreground">Current Staff</h2>
              <p class="mt-1 text-sm text-muted-foreground">Accounts returned by the backend</p>
            </div>
            <button
              type="button"
              class="rounded-lg border border-border px-3 py-2 text-sm font-medium text-foreground transition hover:bg-muted"
              @click="loadUsers"
            >
              Refresh
            </button>
          </div>

          <p v-if="loading" class="mt-4 text-sm text-muted-foreground">Loading staff accounts...</p>

          <div v-else class="mt-4 space-y-3">
            <div
              v-for="user in staffUsers"
              :key="user.id"
              class="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3"
            >
              <div>
                <p class="text-sm font-semibold text-foreground">{{ user.username }}</p>
                <p class="mt-1 text-xs text-muted-foreground">Role: {{ user.role }}</p>
              </div>
              <div class="flex items-center gap-3">
                <span
                  class="rounded-full px-3 py-1 text-xs font-medium"
                  :class="user.has_password ? 'bg-success/10 text-success' : 'bg-muted text-muted-foreground'"
                >
                  {{ user.has_password ? 'Password Set' : 'No Password' }}
                </span>
                <button
                  type="button"
                  class="rounded-lg border border-destructive/30 px-3 py-2 text-xs font-medium text-destructive transition hover:bg-destructive/10 disabled:opacity-60"
                  :disabled="deletingUserId === user.id"
                  @click="handleDeleteStaff(user)"
                >
                  {{ deletingUserId === user.id ? 'Deleting...' : 'Delete' }}
                </button>
              </div>
            </div>

            <p v-if="!staffUsers.length" class="text-sm text-muted-foreground">
              No staff accounts found.
            </p>
          </div>
        </section>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import DashboardLayout from '@/components/DashboardLayout.vue'
import { createStaff, deleteStaff, fetchUsers } from '@/services/owner'

const users = ref([])
const loading = ref(false)
const submitting = ref(false)
const deletingUserId = ref(null)
const errorMessage = ref('')
const successMessage = ref('')
const form = reactive({
  username: '',
  password: '',
})

const staffUsers = computed(() => users.value.filter((user) => user.role === 'staff'))

onMounted(() => {
  loadUsers()
})

async function loadUsers() {
  loading.value = true
  errorMessage.value = ''

  try {
    users.value = await fetchUsers()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not load staff accounts.'
  } finally {
    loading.value = false
  }
}

async function submitStaff() {
  successMessage.value = ''
  errorMessage.value = ''

  if (!form.username.trim() || !form.password) {
    errorMessage.value = 'Username and password are required.'
    return
  }

  submitting.value = true

  try {
    await createStaff({
      username: form.username.trim(),
      password: form.password,
    })

    form.username = ''
    form.password = ''
    successMessage.value = 'Staff account created.'
    await loadUsers()
  } catch (error) {
    const validationMessage = error?.response?.data?.message
    const detail = error?.response?.data?.detail
    errorMessage.value = validationMessage || detail || 'Could not create staff account.'
  } finally {
    submitting.value = false
  }
}

async function handleDeleteStaff(user) {
  successMessage.value = ''
  errorMessage.value = ''

  if (!window.confirm(`Delete staff account "${user.username}"?`)) {
    return
  }

  deletingUserId.value = user.id

  try {
    await deleteStaff(user.id)
    successMessage.value = 'Staff account deleted.'
    users.value = users.value.filter((currentUser) => currentUser.id !== user.id)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not delete staff account.'
  } finally {
    deletingUserId.value = null
  }
}
</script>
