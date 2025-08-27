<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <!-- หัวข้อ -->
    <h1 class="text-3xl font-bold mb-6 text-center text-blue-700">
      ระบบยืม - คืนอุปกรณ์
    </h1>

    <!-- เลือกอุปกรณ์ -->
    <div class="bg-white shadow-lg rounded-lg p-4 mb-6">
      <h2 class="text-lg font-semibold mb-4">เลือกอุปกรณ์</h2>
      <div class="flex space-x-6 overflow-x-auto">
        <div
          v-for="item in devices"
          :key="item.name"
          class="flex flex-col items-center bg-gray-50 p-4 rounded-lg shadow-md w-36"
        >
          <img
            :src="item.image"
            :alt="item.name"
            class="w-20 h-20 object-contain mb-2"
          />
          <p class="font-semibold">{{ item.name }}</p>
          <p class="text-sm text-gray-600">เหลือ: {{ item.count }}</p>
          <button
            @click="addDevice(item)"
            class="mt-2 bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-full disabled:opacity-50"
            :disabled="item.count <= 0"
          >
            ➕
          </button>
        </div>
      </div>
    </div>

    <!-- ฟอร์มเพิ่มรายการยืม -->
    <div class="bg-white shadow-lg rounded-lg p-4 mb-6">
      <h2 class="text-lg font-semibold mb-4">เพิ่มรายการยืมอุปกรณ์</h2>

      <!-- ✅ แสดงอุปกรณ์ที่เลือก -->
      <div v-if="Object.keys(selectedDevices).length" class="mb-4">
        <h3 class="font-semibold mb-2">อุปกรณ์ที่เลือก:</h3>
        <div
          v-for="(qty, name) in selectedDevices"
          :key="name"
          class="flex items-center justify-between bg-gray-50 px-3 py-2 rounded mb-2"
        >
          <span>{{ name }} {{ qty }} ชิ้น</span>
          <div class="space-x-2">
            <button
              @click="decreaseDevice(name)"
              class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded"
            >
              ➖
            </button>
            <button
              @click="increaseDevice(name)"
              class="bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded"
            >
              ➕
            </button>
          </div>
        </div>
      </div>

      <!-- ช่องกรอกข้อมูล -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="title"
          placeholder="สรุปอุปกรณ์ที่ยืม"
          class="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          readonly
        />
        <input
          v-model="borrowerName"
          @keyup.enter="createNote"
          placeholder="ชื่อผู้ยืม"
          class="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="createNote"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          บันทึกการยืม
        </button>
      </div>
    </div>

    <!-- ช่องค้นหา -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        placeholder="ค้นหาชื่อผู้ยืม - อุปกรณ์......."
        class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- รายการอุปกรณ์ที่ถูกยืม -->
    <div class="grid grid-cols-1 gap-4">
      <NoteCard
        v-for="note in filteredNotes"
        :key="note.id"
        :note="note"
        @delete="deleteNote"
      />
    </div>

    <!-- ปุ่ม Logout -->
    <div class="mt-8 text-center">
      <button
        @click="handleLogout"
        class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg shadow"
      >
        ออกจากระบบ
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import NoteCard from '../components/NoteCard.vue'

const title = ref('')
const borrowerName = ref('') // ชื่อผู้ยืม
const notes = ref([])
const searchQuery = ref('')
const router = useRouter()

// ------------------ อุปกรณ์ -------------------
const devices = ref([
  { name: 'ลูกฟุตบอล', image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIHnIGvMnRN2YZkxnwRt1vsKiH_wmqcQaBTQ&s', count: 5 },
  { name: 'ลูกบาส', image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlu6EJW1WF1V8z2_fv8CsD1Dqz7qihsvB-ig&s', count: 3 },
  { name: 'ลูกตะกร้อ', image: 'https://image.makewebcdn.com/makeweb/m_1920x0/RkWxkNYkh/Takraw/Takraw_Green.png', count: 7 },
  { name: 'ลูกแบดมินตัน', image: 'https://png.pngtree.com/png-clipart/20240826/original/pngtree-sport-ball-badminton-png-image_15854112.png', count: 7 },
  { name: 'ลูกเบสบอล', image: 'https://png.pngtree.com/png-clipart/20240808/original/pngtree-ball-baseball-3d-png-image_15723366.png', count: 7 },
  { name: 'ลูกกอล์ฟ', image: 'https://png.pngtree.com/png-vector/20250607/ourmid/pngtree-closeup-of-a-white-golf-ball-on-transparent-background-png-image_16484066.png', count: 7 },
  { name: 'ลูกเทนนิส', image: 'https://png.pngtree.com/png-clipart/20250222/original/pngtree-realistic-3d-tennis-ball-with-textured-surface-for-sports-graphics-and-png-image_20494646.png', count: 7 },
  { name: 'ลูกปิงปอง', image: 'https://png.pngtree.com/png-vector/20231017/ourmid/pngtree-ping-pong-ball---orange-isolated-png-image_10273794.png', count: 7 },
  { name: 'ลูกฟุตซอล', image: 'https://img.th.my-best.com/product_images/00bd316486d65b5fae84e1d8e8f02422.png?ixlib=rails-4.3.1&q=70&lossless=0&w=800&h=800&fit=clip&s=25fb172e36def8344191986708b8b47b', count: 7 },
])

// เก็บจำนวนที่เลือก
const selectedDevices = ref({})

// เพิ่มอุปกรณ์ที่เลือก
const addDevice = (item) => {
  if (item.count > 0) {
    item.count--
    selectedDevices.value[item.name] = (selectedDevices.value[item.name] || 0) + 1
    updateTitle()
  }
}

// เพิ่มในฟอร์ม
const increaseDevice = (name) => {
  const device = devices.value.find(d => d.name === name)
  if (device && device.count > 0) {
    device.count--
    selectedDevices.value[name]++
    updateTitle()
  }
}

// ลดในฟอร์ม
const decreaseDevice = (name) => {
  const device = devices.value.find(d => d.name === name)
  if (device && selectedDevices.value[name] > 0) {
    device.count++
    selectedDevices.value[name]--
    if (selectedDevices.value[name] === 0) {
      delete selectedDevices.value[name]
    }
    updateTitle()
  }
}

// อัปเดตข้อความสรุป
const updateTitle = () => {
  const summary = Object.entries(selectedDevices.value)
    .map(([name, qty]) => `${name} ${qty} ชิ้น`)
    .join(', ')
  title.value = `ยืม : ${summary}\nชื่อ : ${borrowerName.value}`
}

// ✅ อัปเดต title ทุกครั้งที่กรอกชื่อ
watch(borrowerName, () => {
  updateTitle()
})

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
    devices.value.forEach(d => d.count = d.count) // (ถ้า backend มี stock จริงให้ fetch ใหม่แทน)
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchNotes()
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
)

onMounted(fetchNotes)
</script>
