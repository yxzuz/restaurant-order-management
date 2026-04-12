<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
    <div class="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
      <button
        type="button"
        class="absolute right-4 top-4 text-xl text-gray-500 transition hover:text-gray-700"
        @click="$emit('close')"
      >
        ✕
      </button>

      <h2 class="font-heading text-2xl font-bold text-foreground">
        {{ isEditing ? 'Edit Menu Item' : 'Add Menu Item' }}
      </h2>

      <form class="mt-6 space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label class="mb-1 block text-sm font-medium text-foreground">Name</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
          >
        </div>

    <div class="space-y-2">
        <label class="block text-sm font-medium text-foreground">Item Image</label>

        <div
            class="group relative overflow-hidden rounded-2xl border border-border transition-all duration-200"
            :class="isDragging
            ? 'border-orange-400 ring-4 ring-orange-400/10 bg-orange-50/40 dark:bg-orange-900/10'
            : 'bg-muted/20 hover:border-muted-foreground/40 hover:bg-muted/40'"
            @click="openFilePicker"
            @dragenter.prevent="isDragging = true"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
        >
            <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileChange"
            >

            <!-- Image preview state -->
            <div v-if="previewImage" class="relative">
            <img
                :src="previewImage"
                alt="Menu item preview"
                class="h-48 w-full object-cover"
            >
            <!-- Overlay on hover -->
            <div class="absolute inset-0 flex items-center justify-center bg-black/0 transition-all duration-200 group-hover:bg-black/40">
                <button
                type="button"
                class="translate-y-1 scale-95 rounded-xl bg-white/90 px-4 py-2 text-sm font-medium text-gray-900 opacity-0 shadow-lg backdrop-blur-sm transition-all duration-200 group-hover:translate-y-0 group-hover:scale-100 group-hover:opacity-100"
                @click.stop="openFilePicker"
                >
                Replace image
                </button>
            </div>
            </div>
            <!-- Bottom filename bar -->
            <div v-if="previewImage" class="flex items-center gap-2 border-t border-border px-4 py-2.5">
            <svg class="size-3.5 shrink-0 text-muted-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909M3 21h18M3.75 3h16.5M4.5 3v18m15-18v18" />
            </svg>
            <p class="truncate text-xs text-muted-foreground">{{ selectedFileName || 'Current image' }}</p>
            </div>

            <!-- Empty / drop state -->
            <div v-else class="flex flex-col items-center gap-3 px-6 py-12">
            <div
                class="flex size-11 items-center justify-center rounded-xl border border-border bg-background shadow-sm transition-transform duration-200"
                :class="isDragging ? 'scale-110' : 'group-hover:scale-105'"
            >
                <svg class="size-5 text-muted-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                </svg>
            </div>
            <div class="text-center">
                <p class="text-sm font-medium text-foreground">
                {{ isDragging ? 'Drop to upload' : 'Upload an image' }}
                </p>
                <p class="mt-0.5 text-xs text-muted-foreground">Drag and drop, or click to browse</p>
            </div>
            </div>
        </div>
    </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-foreground">Description</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
          />
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="mb-1 block text-sm font-medium text-foreground">Price</label>
            <input
              v-model="form.price"
              type="number"
              min="0"
              step="0.01"
              class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
            >
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium text-foreground">Category</label>
            <select
              v-model="form.category"
              class="w-full rounded-lg border border-input px-3 py-2 outline-none transition focus:border-orange-400"
            >
              <option value="" disabled>Select a category</option>
              <option
                v-for="category in categoryOptions"
                :key="category"
                :value="category"
              >
                {{ category }}
              </option>
            </select>
            <p v-if="categoryError" class="mt-1 text-xs text-red-600">
              {{ categoryError }}
            </p>
          </div>
        </div>

        <div class="flex items-start">          
            <button
            type="button"
            class="inline-flex items-center gap-3 rounded-full px-1 py-1 text-sm font-medium text-foreground transition"
            @click="form.is_available = !form.is_available"
          >
            <span
              class="relative inline-flex h-7 w-12 items-center rounded-full transition-colors"
              :class="form.is_available ? 'bg-orange-500/80' : 'bg-muted'"
            >
              <span
                class="inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform"
                :class="form.is_available ? 'translate-x-6' : 'translate-x-1'"
              />
            </span>
          </button>
          <div>
            <p class="text-sm font-medium py-2 text-foreground">Available</p>
          </div>

        </div>

        <p
          v-if="errorMessage"
          class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {{ errorMessage }}
        </p>

        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            class="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground transition hover:bg-muted"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import api from '@/services/api'

const props = defineProps({
  item: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'save'])

const form = reactive(createForm())
const isEditing = computed(() => !!props.item)
const errorMessage = computed(() => '')
const fileInput = ref(null)
const isDragging = ref(false)
const previewImage = ref('')
const selectedFileName = ref('')
const categoryOptions = ref([])
const categoryError = ref('')
const selectedImageFile = ref(null)
let objectUrl = null

watch(
  () => props.item,
  (item) => {
    Object.assign(form, createForm(item))
    resetPreviewState()
    previewImage.value = item?.image_url ?? ''
    selectedImageFile.value = null
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  clearObjectUrl()
})

onMounted(() => {
  loadCategories()
})

function createForm(item = null) {
  return {
    name: item?.name ?? '',
    description: item?.description ?? '',
    price: item?.price ?? '',
    category: item?.category ?? '',
    image_url: item?.image_url ?? '',
    is_available: item?.is_available ?? true,
  }
}

async function loadCategories() {
  categoryError.value = ''

  try {
    const categories = await api.get('/menus/categories')
    categoryOptions.value = Array.isArray(categories) ? categories : []

    if (!form.category && categoryOptions.value.length > 0) {
      form.category = categoryOptions.value[0]
    }
  } catch {
    categoryOptions.value = []
    categoryError.value = 'Could not load categories from the backend.'
  }
}

function openFilePicker() {
  fileInput.value?.click()
}

function handleFileChange(event) {
  const [file] = event.target.files || []
  applyImageFile(file)
}

function handleDrop(event) {
  isDragging.value = false
  const [file] = event.dataTransfer?.files || []
  applyImageFile(file)
}

function applyImageFile(file) {
  if (!file || !file.type.startsWith('image/')) {
    return
  }

  clearObjectUrl()
  objectUrl = URL.createObjectURL(file)
  previewImage.value = objectUrl
  selectedFileName.value = file.name
  selectedImageFile.value = file
  form.image_url = objectUrl
}

function resetPreviewState() {
  clearObjectUrl()
  selectedFileName.value = ''
  selectedImageFile.value = null
}

function clearObjectUrl() {
  if (objectUrl) {
    URL.revokeObjectURL(objectUrl)
    objectUrl = null
  }
}

function handleSubmit() {
  if (!form.name.trim() || !form.category || form.price === '' || Number(form.price) < 0) {
    return
  }

  emit('save', {
    ...props.item,
    name: form.name.trim(),
    description: form.description.trim(),
    price: Number(form.price),
    category: form.category.trim(),
    image_url: form.image_url.trim(),
    imageFile: selectedImageFile.value,
    is_available: form.is_available,
  })
}
</script>
