<template>
  <div class="poker-container">
    <h1 class="title">ポーカートーナメント検索</h1>
    <div class="search-bar">
      <input
        v-model="searchName"
        class="input"
        type="text"
        placeholder="トーナメント名"
      />
      <input
        v-model.number="bonusMin"
        class="input"
        type="number"
        placeholder="最低賞金"
        min="0"
      />
      <input
        v-model.number="bonusMax"
        class="input"
        type="number"
        placeholder="最高賞金"
        min="0"
      />
      <button @click="onSearch" class="search-btn">
        <span class="icon-search">🔎</span> 検索
      </button>
    </div>

    <div class="result-area">
      <template v-if="loading">
        <div class="loading">トーナメントデータを検索中...</div>
      </template>
      <template v-else-if="results.length">
        <div class="card-list">
          <div
            v-for="event in results"
            :key="event.id"
            class="event-card"
          >
            <div class="event-main">
              <span class="card-title">{{ event.name }}</span>
              <span class="card-bonus">賞金：¥{{ event.bonus }}</span>
            </div>
            <div class="event-detail">
              <span>開催地：{{ event.location || '不明' }}</span>
              <span>日付：{{ event.date || '未公表' }}</span>
            </div>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="no-data">トーナメント情報がありません</div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const searchName = ref('')
const bonusMin = ref('')
const bonusMax = ref('')
const results = ref([])
const loading = ref(false)

async function onSearch() {
  loading.value = true
  try {
    // 'location'は検索項目から除外
    const res = await axios.get('/api/search', {
      params: {
        name: searchName.value,
        bonus_min: bonusMin.value,
        bonus_max: bonusMax.value,
      },
    })
    results.value = res.data?.data || []
  } catch (e) {
    results.value = []
    alert('検索失敗: ' + (e.response?.data?.message || e.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.poker-container {
  max-width: 780px;
  margin: 42px auto 0 auto;
  background: #f7fdfb;
  box-shadow: 0 6px 32px 0 #e0f7ea6b;
  border-radius: 18px;
  padding: 40px 36px 36px 36px;
  box-sizing: border-box;
}
.title {
  text-align: center;
  color: #197144;
  letter-spacing: 2px;
  font-size: 2.4em;
  font-family: 'Montserrat', 'PingFang SC', Arial, sans-serif;
  font-weight: bold;
  margin-bottom: 30px;
}
.search-bar {
  display: flex;
  gap: 18px;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
  background: #fff;
  box-shadow: 0 2px 10px 0 #ceede3a8;
  border-radius: 10px;
  padding: 18px 22px 10px;
}

.input {
  min-width: 140px;
  max-width: 200px;
  flex: 0 1 180px;
  background: #f4fbf6;
  border-radius: 6px;
  border: 1.5px solid #ace8cf;
  outline: none;
  padding: 11px 12px;
  font-size: 1.13em;
  margin-bottom: 8px;
  transition: border-color 0.2s;
}
.input:focus {
  border-color: #40b6a8;
  background: #e3faef;
}
.search-btn {
  background: linear-gradient(90deg, #197144 70%, #49dfaf 100%);
  color: #fff;
  font-weight: 600;
  font-size: 1.17em;
  border: none;
  border-radius: 7px;
  padding: 12px 38px;
  box-shadow: 0 2px 10px #58dfa651;
  cursor: pointer;
  margin-bottom: 8px;
  letter-spacing: 1px;
  transition: opacity 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}
.search-btn:hover {
  opacity: 0.9;
  box-shadow: 0 4px 18px #15704844;
}
.icon-search {
  font-size: 1.34em;
}

.result-area {
  min-height: 200px;
}
.loading {
  text-align: center;
  color: #15a86c;
  font-size: 1.23em;
}
.no-data {
  text-align: center;
  color: #aaa;
  font-size: 1.12em;
  margin-top: 36px;
}

.card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  justify-content: flex-start;
  margin-top: 20px;
}
.event-card {
  background: #fff;
  border-radius: 11px;
  box-shadow: 0 3px 8px #ace8cf45;
  border-left: 6px solid #197144;
  overflow: hidden;
  min-width: 235px;
  max-width: 315px;
  flex: 1 0 260px;
  padding: 22px 20px 16px 20px;
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
  transition: transform 0.15s;
}
.event-card:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 10px 28px #58dfa631;
}
.card-title {
  color: #197144;
  font-weight: 700;
  font-size: 1.16em;
  letter-spacing: 1.5px;
}
.card-bonus {
  color: #28bb70;
  font-size: 1.12em;
  font-family: Monaco, monospace;
  font-weight: 600;
  margin-left: 8px;
}
.event-detail {
  color: #287061;
  font-size: 0.98em;
  margin-top: 9px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

@media (max-width: 850px) {
  .poker-container {
    padding: 22px 6px 28px 6px;
  }
  .search-bar {
    padding: 10px 3vw;
    gap: 10px;
  }
  .card-list {
    justify-content: center;
  }
}
@media (max-width: 650px) {
  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>