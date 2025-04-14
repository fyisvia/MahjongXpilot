<template>
  <el-menu mode="horizontal" background-color="#409eff" text-color="#fff" active-text-color="#ffd04b">
    <el-menu-item index="1">
      <router-link to="/">首页</router-link>
    </el-menu-item>
    <el-menu-item index="2">
      <router-link to="/replay">牌谱分析</router-link>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
</script>

<style scoped>
a {
  color: white;
  text-decoration: none;
}
</style>