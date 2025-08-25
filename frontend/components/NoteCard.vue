<template>
  <div class="bg-white p-4 shadow rounded mb-3 flex justify-between items-center">
    <div>
      <h2 class="font-bold whitespace-pre-line">{{ note.title }}</h2>
      <p class="text-xs text-gray-500">{{ note.created_at }}</p>
    </div>
    <div class="flex flex-col items-end space-y-2">
      <!-- สถานะคืนอุปกรณ์ -->
      <span 
        :class="note.returned === note.amount ? 'text-green-600' : 'text-red-600'" 
        class="text-sm font-semibold"
      >
        {{ note.returned === note.amount ? 'คืนแล้ว' : 'ยังไม่คืน' }}
      </span>

      <div class="flex space-x-2">
        <button 
          @click="$emit('update', note.id)" 
          class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm"
        >
          Update
        </button>
        <button 
          @click="$emit('delete', note.id)" 
          class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ note: Object })
defineEmits(['delete', 'update'])
</script>
  