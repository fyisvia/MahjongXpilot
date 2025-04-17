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
    <div v-if="parseResult" class="result">
      <h2>对局信息</h2>
      <p>玩家：{{ parseResult.players.join(', ') }}</p>
      <p>得分：{{ parseResult.scores }}</p>
      <div v-if="parseResult.tiles" class="tiles">
        <h3>牌面</h3>
        <svg
          v-for="tile in parseResult.tiles"
          :key="tile"
          width="40"
          height="60"
          class="tile"
        >
          <rect width="40" height="60" fill="white" stroke="black" rx="5" />
          <text
            x="20"
            y="30"
            text-anchor="middle"
            font-size="14"
            :fill="getTileColor(tile)"
          >
            {{ getTileText(tile) }}
          </text>
        </svg>
      </div>
      <div v-if="parseResult.actions" class="replay">
        <h3>对局回放</h3>
        <p v-if="currentStep >= 0">
          第 {{ currentStep + 1 }} 步：{{ parseResult.actions[currentStep].type === 'T' ? '摸牌' : parseResult.actions[currentStep].type === 'D' ? '打牌' : '立直' }} {{ parseResult.actions[currentStep].tile }}
        </p>
        <el-button @click="prevStep" :disabled="currentStep <= 0">上一轮</el-button>
        <el-button @click="nextStep" :disabled="currentStep >= parseResult.actions.length - 1">下一轮</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

interface ParseResult {
  players: string[];
  scores: string;
  tiles?: string[];
  actions?: { type: string; tile: string }[];
}

const parseResult = ref<ParseResult | null>(null)
const currentStep = ref(-1)

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
  try {
    const parseResponse = await axios.get(`/api/parse/${response.filename}`)
    console.log('Parse result:', parseResponse.data)
    parseResult.value = parseResponse.data.data
    currentStep.value = 0 // 初始化回放
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

const nextStep = () => {
  if (parseResult.value && parseResult.value.actions?.length && currentStep.value < parseResult.value.actions.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 麻将牌文本（显示中文或符号）
const getTileText = (tile: string) => {
  if (tile.includes('m')) return tile.replace('m', '萬')
  if (tile.includes('p')) return tile.replace('p', '筒')
  if (tile.includes('s')) return tile.replace('s', '索')
  switch (tile) {
    case 'Haku': return '白'
    case 'Hatsu': return '発'
    case 'Chun': return '中'
    case 'Ton': return '東'
    case 'Nan': return '南'
    case 'Shaa': return '西'
    case 'Pei': return '北'
    default: return tile
  }
}

// 麻将牌颜色（区分牌类型）
const getTileColor = (tile: string) => {
  if (tile.includes('m')) return 'red' // 万
  if (tile.includes('p')) return 'blue' // 筒
  if (tile.includes('s')) return 'green' // 索
  return 'black' // 字牌
}
</script>

<style scoped>
.upload-demo {
  margin-top: 20px;
}
.result {
  margin-top: 20px;
}
.tiles {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.tile {
  width: 40px;
  height: 60px;
}
.replay {
  margin-top: 20px;
}
</style>