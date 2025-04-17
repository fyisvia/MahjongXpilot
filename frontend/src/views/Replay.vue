<template>
  <div class="replay-container">
    <h1>牌谱回放</h1>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="parseResult" class="result">
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
    <el-button type="primary" @click="goBack">返回主页</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
interface ParseResult {
  players: string[];
  scores: string;
  tiles?: string[];
  actions?: { type: string; tile: string }[];
}

const parseResult = ref<ParseResult | null>(null)
const currentStep = ref(-1)
const loading = ref(true)
const error = ref('')

// 获取牌谱数据
const fetchReplay = async () => {
  const filename = route.params.filename as string
  if (!filename) {
    error.value = '未提供牌谱文件名'
    loading.value = false
    return
  }
  try {
    const response = await axios.get(`/api/parse/${filename}`)
    parseResult.value = response.data.data
    currentStep.value = 0 // 初始化回放
    ElMessage.success('牌谱加载成功！')
  } catch (err) {
    console.error('Fetch error:', err)
    const errorMessage = (err as any)?.response?.data?.error || (err as Error).message;
    error.value = '加载牌谱失败：' + errorMessage;
    ElMessage.error('牌谱加载失败！')
  } finally {
    loading.value = false
  }
}

// 麻将牌文本
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

// 麻将牌颜色
const getTileColor = (tile: string) => {
  if (tile.includes('m')) return 'red' // 万
  if (tile.includes('p')) return 'blue' // 筒
  if (tile.includes('s')) return 'green' // 索
  return 'black' // 字牌
}

// 回放控制
const nextStep = () => {
  if (parseResult.value && parseResult.value.actions && currentStep.value < parseResult.value.actions.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 返回主页
const goBack = () => {
  router.push('/')
}

// 页面加载时获取数据
onMounted(() => {
  fetchReplay()
})
</script>

<style scoped>
.replay-container {
  padding: 20px;
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
.error {
  color: red;
  margin-top: 20px;
}
</style>