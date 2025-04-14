<template>
  <el-container>
    <el-header>
      <Header />
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import Header from './components/Header.vue'
</script>

<style scoped>
.el-container {
  min-height: 100vh;
}
.el-header {
  background-color: #409eff;
  color: white;
  line-height: 60px;
}
</style>