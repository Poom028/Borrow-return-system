<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <div class="container mx-auto px-6 py-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">รายชื่อสมาชิก</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div v-for="member in members" :key="member.code" class="bg-white/90 rounded-2xl shadow-lg p-6 flex items-center border border-white/30 hover:scale-[1.03] transition-transform">
          <div class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-200 via-indigo-200 to-purple-200 flex items-center justify-center text-2xl font-bold text-indigo-700 mr-6 shadow">
            {{ member.avatar }}
          </div>
          <div>
            <div class="text-xl font-semibold text-gray-900">{{ member.name }}</div>
            <div class="text-gray-500 text-sm mt-1">รหัสสมาชิก: {{ member.code }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const members = [
  { name: 'นายพายุ สาลีศรี', code: '028', avatar: 'พ' },
  { name: 'นายจิรายุ ทองอุดมศิริ', code: '018', avatar: 'จ' },
  { name: 'นายฐิติภัทร จูมจะนะ', code: '019', avatar: 'ฐ' },
  { name: 'นายวีรภัทร หอมภักดี', code: '032', avatar: 'ว' },
]
</script>