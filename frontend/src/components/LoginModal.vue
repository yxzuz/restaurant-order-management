<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

    <!-- Box -->
    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md relative">

      <!-- Close button -->
      <button
        @click="$emit('close')"
        class="absolute top-2 right-3 text-gray-500"
      >
        ✕
      </button>

      <h2 class="text-2xl font-bold text-center mb-6">
        {{ title }} Access
      </h2>

      <div
        v-if="requiredRole === 'owner'"
        class="mb-4 grid grid-cols-2 gap-2 rounded-lg border border-gray-200 p-1"
      >
        <button
          type="button"
          @click="mode = 'login'"
          :class="[
            'rounded-md px-3 py-2 text-sm font-medium transition',
            mode === 'login' ? 'bg-[#2a221d] text-white' : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          Login
        </button>
        <button
          type="button"
          @click="mode = 'create'"
          :class="[
            'rounded-md px-3 py-2 text-sm font-medium transition',
            mode === 'create' ? 'bg-[#2a221d] text-white' : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          Create account
        </button>
      </div>

      <p
        v-if="requiredRole === 'owner'"
        class="mb-4 text-xs text-gray-500"
      >
        Use "Create account" only for first-time owner setup.
      </p>

      <p
        v-if="errorMessage"
        class="mb-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
      >
        {{ errorMessage }}
      </p>

      <form @submit.prevent="handleLogin">

        <input
          v-model="username"
          type="text"
          placeholder="Username"
          class="w-full mb-4 p-3 border rounded"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full mb-6 p-3 border rounded"
        />

        <button :disabled="loading" class="w-full bg-[#2a221d] text-white p-3 rounded disabled:opacity-60">
          {{ loading ? 'Please wait...' : submitLabel }}
        </button>

      </form>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import api from '@/services/api'

const props = defineProps({
  requiredRole: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['close', 'success'])

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)
const mode = ref('login')

const title = computed(() => {
  if (props.requiredRole === 'owner') return 'Owner'
  if (props.requiredRole === 'staff') return 'Staff'
  return 'User'
})

const submitLabel = computed(() => {
  if (props.requiredRole === 'owner' && mode.value === 'create') {
    return 'Create owner account'
  }
  return 'Login'
})

async function handleLogin() {
  errorMessage.value = ''
  loading.value = true

  try {
    const payload = {
      username: username.value.trim(),
      password: password.value,
    }

    if (!payload.username || !payload.password) {
      errorMessage.value = 'Please enter both username and password.'
      return
    }

    if (props.requiredRole === 'owner' && mode.value === 'create') {
      await api.post('/auth/bootstrap-owner', payload)
    }

    const tokenResponse = await api.post('/auth/login', payload)
    const accessToken = tokenResponse.access_token
    if (!accessToken) {
      throw new Error('Login token missing')
    }

    localStorage.setItem('token', accessToken)

    const me = await api.get('/auth/me')
    if (props.requiredRole && me.role !== props.requiredRole) {
      localStorage.removeItem('token')
      localStorage.removeItem('user_role')
      errorMessage.value = `This account is ${me.role}. Please use a ${props.requiredRole} account.`
      return
    }

    localStorage.setItem('user_role', me.role)
    emit('success', { role: me.role })
  } catch (error) {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail
    const validationMessage = error?.response?.data?.message

    // Handle validation errors (400 with friendly message)
    if (status === 400 && validationMessage) {
      errorMessage.value = validationMessage
      return
    }

    if (status === 400 && props.requiredRole === 'owner' && mode.value === 'create') {
      if (typeof detail === 'string' && detail.toLowerCase().includes('already exists')) {
        errorMessage.value = 'Owner account already exists. Please switch to Login.'
      } else {
        errorMessage.value = detail || 'Could not create owner account. Please check your details.'
      }
      return
    }

    if (status === 401) {
      errorMessage.value = 'Invalid username or password.'
      return
    }

    if (!error?.response) {
      errorMessage.value = 'Cannot reach server. Please make sure backend is running.'
      return
    }

    errorMessage.value = detail || 'Request failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>