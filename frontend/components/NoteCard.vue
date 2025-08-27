<template>
  <div class="bg-gradient-to-r from-white to-gray-50 p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-blue-200 group">
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
      <!-- Content Section -->
      <div class="flex-1">
        <div class="flex items-start space-x-4">
          <!-- Status Indicator -->
          <div class="flex-shrink-0">
            <div 
              :class="note.status === 'Returned' ? 'bg-green-100 border-green-300' : 'bg-red-100 border-red-300'"
              class="w-12 h-12 rounded-full border-2 flex items-center justify-center"
            >
              <svg 
                :class="note.status === 'Returned' ? 'text-green-600' : 'text-red-600'"
                class="w-6 h-6" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  v-if="note.status === 'Returned'"
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M5 13l4 4L19 7"
                />
                <path 
                  v-else
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
            </div>
          </div>

          <!-- Note Details -->
          <div class="flex-1 min-w-0">
            <h3 class="font-bold text-gray-800 text-lg mb-2 leading-relaxed whitespace-pre-line">
              {{ note.title }}
            </h3>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                {{ note.created_at }}
              </div>
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                {{ note.content }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions Section -->
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-3 sm:space-y-0 sm:space-x-3">
        <!-- Status Display -->
        <div class="flex items-center justify-center">
          <span 
            :class="note.status === 'Returned' ? 'bg-green-100 text-green-800 border-green-200' : 'bg-red-100 text-red-800 border-red-200'"
            class="px-4 py-2 rounded-full text-sm font-semibold border-2"
          >
            {{ note.status === 'Returned' ? 'คืนแล้ว' : 'ยังไม่คืน' }}
          </span>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-2">
          <!-- Status Update Dropdown -->
          <div class="relative" v-if="showStatusDropdown">
            <select
              v-model="selectedStatus"
              @change="updateStatus"
              class="bg-gradient-to-r from-pink-500 to-indigo-500 text-black-500 px-4 py-2 rounded-lg text-sm font-medium appearance-none cursor-pointer pr-10 transition-all duration-200 shadow-md hover:scale-105"
            >
              <option value="Not Returned" >ยังไม่คืน</option>
              <option value="Returned" >คืนแล้ว</option>
            </select>
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>
          </div>

          <!-- Update Button -->
          <button 
            v-if="!showStatusDropdown"
            @click="showStatusDropdown = true" 
            class="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-md flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Update
          </button>

          <!-- Cancel Button -->
          <button 
            v-if="showStatusDropdown"
            @click="cancelUpdate" 
            class="bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-md flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            Cancel
          </button>

          <!-- Delete Button -->
          <button 
            @click="$emit('delete', note.id)" 
            class="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-md flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({ note: Object })
const emit = defineEmits(['delete', 'update'])

const showStatusDropdown = ref(false)
const selectedStatus = ref('')

onMounted(() => {
  selectedStatus.value = props.note.status || 'Not Returned'
})

const updateStatus = async () => {
  if (selectedStatus.value !== props.note.status) {
    emit('update', props.note.id, { status: selectedStatus.value })
    showStatusDropdown.value = false
  } else {
    showStatusDropdown.value = false
  }
}

const cancelUpdate = () => {
  selectedStatus.value = props.note.status || 'Not Returned'
  showStatusDropdown.value = false
}
</script>
  