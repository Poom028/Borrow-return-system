<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <nav class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white px-6 py-4 flex justify-between items-center">
      <NuxtLink to="/" class="font-bold text-xl">ระบบยืม - คืนอุปกรณ์</NuxtLink>
      <div class="space-x-4">
        <NuxtLink to="/login">เข้าสู่ระบบ</NuxtLink>
        <NuxtLink to="/dashboard">ยืมอุปกรณ์</NuxtLink>
        <NuxtLink to="/members" class="font-semibold underline">รายชื่อสมาชิก</NuxtLink>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">รายชื่อสมาชิก</h1>
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-white/20">
        <ul class="space-y-6 text-gray-800 text-lg">
          <li>
            <div>นายพายุ สาลีศรี 028</div>
          </li>
          <li>
            <div>นายจิรายุ 018</div>
          </li>
          <li>
            <div>นายฐิติภัทร 019</div>
          </li>
          <li>
            <div>นายวีรภัทร 032</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
  
</template>


