<template>
  <div class="p-6 max-w-3xl mx-auto">
    <!-- หัวข้อ -->
    <h1 class="text-2xl font-bold mb-4">My Notes</h1>

    <!-- แถบเพิ่มโน้ต -->
    <div class="flex gap-2 mb-4">
      <input v-model="title" placeholder="Title" class="border p-2 w-1/3" />
      <input v-model="content" placeholder="Content" class="border p-2 flex-1" />
      <button @click="createNote" class="bg-green-500 text-white p-2">Add</button>
    </div>

    <!-- ช่องค้นหา -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        placeholder="Search notes..."
        class="border p-2 w-full"
      />
    </div>

    <!-- รายการโน้ต -->
    <NoteCard
      v-for="note in filteredNotes"
      :key="note.id"
      :note="note"
      @delete="deleteNote"
    />

    <!-- ปุ่ม Logout -->
    <div class="mt-8 text-center">
      <button
        @click="handleLogout"
        class="bg-red-500 text-white px-6 py-2 rounded hover:bg-red-600"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NoteCard from '../components/NoteCard.vue'

const title = ref('')
const content = ref('')
const notes = ref([])
const searchQuery = ref('')

const router = useRouter()

const fetchNotes = async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  const token = localStorage.getItem('token')
  try {
    await axios.post(
      'http://localhost:5000/api/notes',
      {
        title: title.value,
        content: content.value
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    title.value = ''
    content.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const filteredNotes = computed(() => {
  return notes.value.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      note.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(fetchNotes)
</script>
