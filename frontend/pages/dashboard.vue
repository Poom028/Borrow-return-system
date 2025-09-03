<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Header Section -->
    

    <div class="container mx-auto px-6 py-8">
      <!-- Equipment Selection Section -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-8 border border-white/20">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center mr-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">เลือกอุปกรณ์</h2>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div
            v-for="item in devices"
            :key="item.name"
            class="group bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100"
          >
            <div class="flex flex-col items-center text-center">
              <div class="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mb-1 group-hover:scale-110 transition-transform duration-300">
                <img
                  :src="getEquipmentImage(item.name)"
                  :alt="item.name"
                  class="w-16 h-16 object-contain"
                  @error="handleImageError"
                  @load="handleImageLoad"
                />
              </div>
              <h3 class="font-semibold text-gray-800 mb-2 text-sm">{{ item.name }}</h3>
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-2 h-2 rounded-full" :class="item.quantity > 0 ? 'bg-green-500' : 'bg-red-500'"></div>
                <span class="text-sm font-medium" :class="item.quantity > 0 ? 'text-green-600' : 'text-red-600'">
                  เหลือ: {{ item.quantity }}
                </span>
              </div>
              <button
                @click="addDevice(item)"
                class="w-full bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white px-4 py-2 rounded-lg font-medium transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                :disabled="item.quantity <= 0"
              >
                <span class="flex items-center justify-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  เลือก
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Borrowing Form Section -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-8 border border-white/20">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mr-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">เพิ่มรายการยืมอุปกรณ์</h2>
        </div>

        <!-- Selected Equipment Display -->
        <div v-if="Object.keys(selectedDevices).length" class="mb-6">
          <h3 class="font-semibold mb-4 text-gray-700 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
            อุปกรณ์ที่เลือก:
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="(qty, name) in selectedDevices"
              :key="name"
              class="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-200 flex items-center justify-between"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                  <span class="text-white text-sm font-bold">{{ qty }}</span>
                </div>
                <span class="font-medium text-gray-700">{{ name }}</span>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="decreaseDevice(name)"
                  class="w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-lg flex items-center justify-center transition-colors duration-200"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
                  </svg>
                </button>
                <button
                  @click="increaseDevice(name)"
                  class="w-8 h-8 bg-blue-500 hover:bg-blue-600 text-white rounded-lg flex items-center justify-center transition-colors duration-200"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Form -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">สรุปอุปกรณ์ที่ยืม</label>
            <input
              v-model="title"
              placeholder="สรุปอุปกรณ์ที่ยืม"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50"
              readonly
            />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">ชื่อผู้ยืม</label>
            <input
              v-model="borrowerName"
              @keyup.enter="createNote"
              placeholder="ชื่อผู้ยืม"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">&nbsp;</label>
            <button
              @click="createNote"
              class="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 flex items-center justify-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              บันทึกการยืม
            </button>
          </div>
        </div>
      </div>

      <!-- Search Section -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 mb-8 border border-white/20">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <h2 class="text-xl font-bold text-gray-800">ค้นหา</h2>
        </div>
        <input
          v-model="searchQuery"
          placeholder="ค้นหาชื่อผู้ยืม - อุปกรณ์......."
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-white"
        />
      </div>

      <!-- Borrowed Equipment List -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-white/20">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center mr-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">รายการอุปกรณ์ที่ถูกยืม</h2>
        </div>
        
        <div class="space-y-4">
          <NoteCard
            v-for="note in filteredNotes"
            :key="note._id"
            :note="note"
            @delete="deleteNote"
            @update="updateNote"
          />
        </div>
      </div>

      <!-- Logout Section -->
      <div class="text-center mt-12">
        <button
          @click="handleLogout"
          class="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white px-8 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
        >
          <span class="flex items-center justify-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            ออกจากระบบ
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import NoteCard from '../components/NoteCard.vue'

const title = ref('')
const borrowerName = ref('')
const notes = ref([])
const searchQuery = ref('')
const router = useRouter()

// ------------------ อุปกรณ์ -------------------
const devices = ref([])

// เก็บจำนวนที่เลือก
const selectedDevices = ref({})

// Fetch equipment data from backend
const fetchEquipment = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/equipment/public')
    devices.value = response.data
  } catch (error) {
    console.error('Failed to fetch equipment:', error)
    // Fallback to default devices if API fails
    devices.value = [
      { name: 'ลูกฟุตบอล', quantity: 10 },
      { name: 'ลูกบาส', quantity: 10 },
      { name: 'ลูกตะกร้อ', quantity: 10 },
      { name: 'ลูกแบดมินตัน', quantity: 10 },
      { name: 'ลูกเบสบอล', quantity: 10 },
      { name: 'ลูกกอล์ฟ', quantity: 10 },
      { name: 'ลูกเทนนิส', quantity: 10 },
      { name: 'ลูกปิงปอง', quantity: 10 },
      { name: 'ลูกฟุตซอล', quantity: 10 },
      { name: 'ลูกวอลเล่บอล', quantity: 10 },
    ]
  }
}

// Get equipment image based on name
const getEquipmentImage = (name) => {
  const imageMap = {
    'ลูกฟุตบอล': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIHnIGvMnRN2YZkxnwRt1vsKiH_wmqcQaBTQ&s',
    'ลูกบาส': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlu6EJW1WF1V8z2_fv8CsD1Dqz7qihsvB-ig&s',
    'ลูกตะกร้อ': 'https://image.makewebcdn.com/makeweb/m_1920x0/RkWxkNYkh/Takraw/Takraw_Green.png',
    'ลูกแบดมินตัน': 'https://png.pngtree.com/png-clipart/20240826/original/pngtree-sport-ball-badminton-png-image_15854112.png',
    'ลูกเบสบอล': 'https://png.pngtree.com/png-clipart/20240808/original/pngtree-ball-baseball-3d-png-image_15723366.png',
    'ลูกกอล์ฟ': 'https://png.pngtree.com/png-vector/20250607/ourmid/pngtree-closeup-of-a-white-golf-ball-on-transparent-background-png-image_16484066.png',
    'ลูกเทนนิส': 'https://png.pngtree.com/png-clipart/20250222/original/pngtree-realistic-3d-tennis-ball-with-textured-surface-for-sports-graphics-and-png-image_20494646.png',
    'ลูกปิงปอง': 'https://png.pngtree.com/png-vector/20231017/ourmid/pngtree-ping-pong-ball---orange-isolated-png-image_10273794.png',
    'ลูกฟุตซอล': 'https://img.th.my-best.com/product_images/00bd316486d65b5fae84e1d8e8f02422.png?ixlib=rails-4.3.1&q=70&lossless=0&w=800&h=800&fit=clip&s=25fb172e36def8344191986708b8b47b',
    'ลูกวอลเล่บอล': 'https://img.th.my-best.com/product_images/bb7d665360da64af5541c7f07af9da2b.png?ixlib=rails-4.3.1&q=70&lossless=0&w=800&h=800&fit=clip&s=be46c00e232bb00365a4d27d12054418',
  }
  return imageMap[name] || 'https://via.placeholder.com/80x80/4F46E5/FFFFFF?text=Equipment'
}

// Handle image loading errors
const handleImageError = (event) => {
  console.warn('Image failed to load:', event.target.src)
  // Set fallback image
  event.target.src = 'https://via.placeholder.com/80x80/4F46E5/FFFFFF?text=Equipment'
}

// Handle successful image loading
const handleImageLoad = (event) => {
  console.log('Image loaded successfully:', event.target.src)
}

// เพิ่มอุปกรณ์ที่เลือก
const addDevice = (item) => {
  if (item.quantity > 0) {
    item.quantity--
    selectedDevices.value[item.name] = (selectedDevices.value[item.name] || 0) + 1
    updateTitle()
  }
}

// เพิ่มในฟอร์ม
const increaseDevice = (name) => {
  const device = devices.value.find(d => d.name === name)
  if (device && device.quantity > 0) {
    device.quantity--
    selectedDevices.value[name]++
    updateTitle()
  }
}

// ลดในฟอร์ม
const decreaseDevice = (name) => {
  const device = devices.value.find(d => d.name === name)
  if (device && selectedDevices.value[name] > 0) {
    device.quantity++
    selectedDevices.value[name]--
    if (selectedDevices.value[name] === 0) {
      delete selectedDevices.value[name]
    }
    updateTitle()
  }
}

// ✅ อัปเดตข้อความสรุป
const updateTitle = () => {
  const summary = Object.entries(selectedDevices.value)
    .map(([name, qty]) => `${name} ${qty} ชิ้น`)
    .join(', ')
  title.value = summary
    ? `ยืม : ${summary} \nชื่อ : ${borrowerName.value || '...'}`
    : ''
}

// ✅ อัปเดต title ทุกครั้งที่กรอกชื่อหรือเปลี่ยนจำนวน
watch([selectedDevices, borrowerName], () => {
  updateTitle()
}, { deep: true })

// ------------------------------------------------

const fetchNotes = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  try {
    const res = await axios.get('http://localhost:5000/api/notes', {
      headers: { Authorization: `Bearer ${token}` }
    })
    notes.value = res.data
  } catch (e) {
    console.error('Fetch failed:', e)
    handleLogout()
  }
}

const createNote = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }

  if (!Object.keys(selectedDevices.value).length || !borrowerName.value) {
    alert('กรุณาเลือกอุปกรณ์ และกรอกชื่อผู้ยืม')
    return
  }

  try {
    await axios.post(
      'http://localhost:5000/api/notes',
      { title: title.value, content: borrowerName.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )

    title.value = ''
    borrowerName.value = ''
    selectedDevices.value = {}
    
    // Refresh equipment data from backend to get updated quantities
    await fetchEquipment()
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  try {
    await axios.delete(`http://localhost:5000/api/notes/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    // Refresh both notes and equipment data
    await fetchEquipment()
    fetchNotes()
  } catch (error) {
    console.error('Delete note failed:', error)
  }
}


const updateNote = async (id, updatedNote) => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  try {
    await axios.put(`http://localhost:5000/api/notes/${id}`, updatedNote, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchNotes() // Refresh notes to get updated status
    // No need to refresh equipment here, as status change doesn't affect quantity
  } catch (error) {
    console.error('Update note failed:', error)
  }
}

const handleLogout = () => {
  if (confirm("คุณแน่ใจหรือไม่ว่าต้องการออกจากระบบ?")) {
    localStorage.removeItem('token')
    router.push('/login')
  }
}

const filteredNotes = computed(() =>
  notes.value.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      note.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)//gddfg
onMounted(async () => {
  await fetchEquipment()
  fetchNotes()
})
</script>
