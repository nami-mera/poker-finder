<template>
  <div class="container">
    <h1 class="title">POKER-FINDER</h1>

    <div class="search-bar">
      <select v-model="search.reward_categories" class="input-field">
        <option value="">全部奖金类型</option>
        <option v-for="category in rewardCategories" :key="category" :value="category">{{ category }}</option>
      </select>

      <input
        v-model.number="search.minTotal"
        type="number"
        placeholder="最小总奖金 (JPY)"
        class="input-field"
        min="0"
      />
      <input
        v-model.number="search.maxTotal"
        type="number"
        placeholder="最大总奖金 (JPY)"
        class="input-field"
        min="0"
      />

      <button @click="onSearch" class="search-button">查询</button>
    </div>

    <div class="result-list" v-if="results.length > 0">
      <table>
        <thead>
          <tr>
            <th>奖金类型</th>
            <th>总奖金 (JPY)</th>
            <th>事件名称</th>
            <th>开始时间</th>
            <th>状态</th>
            <th>活动链接</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.event_id">
            <td>{{ item.reward_categories }}</td>
            <td>{{ item.total_value_jpy.toLocaleString() }}</td>
            <td>{{ item.event_name }}</td>
            <td>{{ formatDate(item.start_time) }}</td>
            <td>
              <span :class="['status', statusClass(item.status)]">{{ item.status }}</span>
            </td>
            <td>
              <a :href="item.event_link" target="_blank" rel="noopener" class="event-link">查看详情</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-results">
      暂无查询结果
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const rewardCategories = ref([
  '现金', '代金券', '实物礼品', '积分', 'ticket', 'coin', '其他'
])

const search = reactive({
  reward_categories: '',
  minTotal: null,
  maxTotal: null
})

const results = ref([])

// 构建查询参数字符串
function buildQueryParams() {
  const params = new URLSearchParams()

  if (search.reward_categories) {
    params.append('reward_categories', search.reward_categories)
  }
  if (search.minTotal != null && !isNaN(search.minTotal)) {
    params.append('min_total_value_jpy', search.minTotal)
  }
  if (search.maxTotal != null && !isNaN(search.maxTotal)) {
    params.append('max_total_value_jpy', search.maxTotal)
  }
  return params.toString()
}

async function onSearch() {
  try {
    const query = buildQueryParams()
    const API_BASE_URL = import.meta.env.VITE_API_URL;
    console.log(API_BASE_URL);
    const res = await fetch(`${API_BASE_URL}/api/tournament/?${query}`);
    if (!res.ok) {
      console.error('请求失败', res.status)
      results.value = []
      return
    }
    const json = await res.json()
    results.value = json.data  // 取 data 数组
  } catch (error) {
    console.error('请求异常', error)
    results.value = []
  }
}

function formatDate(datetimeStr) {
  if (!datetimeStr) return '-'
  const date = new Date(datetimeStr)
  return date.toLocaleString()
}

function statusClass(status) {
  switch (status) {
    case '待機中':
      return 'status-pending'
    case '进行中':
      return 'status-active'
    case '已结束':
      return 'status-ended'
    default:
      return ''
  }
}
</script>

<style scoped>
.container {
  max-width: 960px;
  margin: 3rem auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.8rem;
  text-align: center;
  user-select: none;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.input-field {
  padding: 0.5rem 0.75rem;
  font-size: 1.05rem;
  border: 1.8px solid #ced4da;
  border-radius: 8px;
  flex: 1 1 180px;
  min-width: 140px;
  transition: border-color 0.25s;
}

.input-field:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 5px #66b1ffaa;
}

.search-button {
  background: linear-gradient(135deg, #40a9ff 0%, #096dd9 100%);
  color: #fff;
  border: none;
  padding: 0.6rem 1.8rem;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  border-radius: 10px;
  min-width: 110px;
  user-select: none;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
  transition: background 0.3s ease;
}

.search-button:hover {
  background: linear-gradient(135deg, #69c0ff, #0050b3);
}

.result-list table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 0.8rem;
  font-size: 1rem;
  user-select: text;
}

.result-list thead tr {
  background-color: #fafafa;
  box-shadow: inset 0 -3px 8px #e2e6eb;
  user-select: none;
}

.result-list th,
.result-list td {
  padding: 0.75rem 1.2rem;
  text-align: left;
  vertical-align: middle;
  color: #2c3e50;
}

.result-list th {
  font-weight: 600;
  font-size: 1.05rem;
}

.result-list tbody tr {
  background-color: #fefefe;
  border-radius: 8px;
  transition: transform 0.18s ease;
}

.result-list tbody tr:hover {
  background-color: #e6f7ff;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgb(24 144 255 / 0.15);
}

.status {
  padding: 0.25rem 0.8rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  color: white;
  display: inline-block;
  user-select: none;
}

.status-pending {
  background-color: #faad14;
}

.status-active {
  background-color: #52c41a;
}

.status-ended {
  background-color: #f5222d;
}

.event-link {
  color: #1890ff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.event-link:hover {
  text-decoration: underline;
  color: #0050b3;
}

.no-results {
  color: #888;
  font-size: 1.2rem;
  font-style: italic;
  text-align: center;
  margin-top: 4rem;
  user-select: none;
}
</style>