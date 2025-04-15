<template>
  <div>
    <h1>MahjongXpilot</h1>
    <el-button type="primary" @click="testApi">测试API</el-button>
    <el-upload
      class="upload-demo"
      action="/api/upload"
      :on-success="handleUploadSuccess"
      :on-error="handleUploadError"
      accept=".mjlog,.xml"
      :limit="1"
    >
      <el-button type="primary">上传牌谱</el-button>
      <template #tip>
        <div class="el-upload__tip">
          请上传天凤牌谱文件（.mjlog 或 .xml）
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

const uploadedFilename = ref('')

const testApi = async () => {
  try {
    const response = await axios.get('/api/replay')
    console.log('Response:', response.data)
    ElMessage.success('API调用成功！')
  } catch (error) {
    console.error('Error:', error)
    ElMessage.error('API调用失败！')
  }
}

const handleUploadSuccess = async (response: any) => {
  console.log('Upload response:', response)
  ElMessage.success('牌谱上传成功！')
  uploadedFilename.value = response.filename
  // 调用解析接口
  try {
    const parseResponse = await axios.get(`/api/parse/${response.filename}`)
    console.log('Parse result:', parseResponse.data)
    ElMessage.success('牌谱解析成功！')
  } catch (error) {
    console.error('Parse error:', error)
    ElMessage.error('牌谱解析失败！')
  }
}

const handleUploadError = (error: any) => {
  console.error('Upload error:', error)
  ElMessage.error('牌谱上传失败！')
}
</script>

<style scoped>
.upload-demo {
  margin-top: 20px;
}
</style>