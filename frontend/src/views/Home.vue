<template>
  <div>
    <h1>Welcome to MahjongXpilot</h1>
    <el-button type="primary" @click="testApi">测试API</el-button>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ElMessage } from 'element-plus'

const testApi = async () => {
  try {
    const response = await axios.get('/api/replay')
    console.log('Response data:', response.data)
    ElMessage.success('API调用成功！')
  } catch (error) {
    console.error('Error:', error)
    ElMessage.error('API调用失败！')
  }
}
</script>