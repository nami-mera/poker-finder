<template>
  <div>
    <!-- フィルター -->
    <el-form :inline="true" :model="filters" @submit.prevent>
      <el-form-item label="開催期間">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          start-placeholder="開始日"
          end-placeholder="終了日"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :default-value="defaultRange"
          style="width: 240px"/>
      </el-form-item>
      <el-form-item label="参加費用">
        <el-input-number v-model="filters.entry_fee_min" :placeholder="'最小'" :min="0" style="width:100px" />
        <span style="margin: 0 4px;">〜</span>
        <el-input-number v-model="filters.entry_fee_max" :placeholder="'最大'" :min="0" style="width:100px" />
      </el-form-item>
      <el-form-item label="キーワード">
        <el-input v-model="filters.keyword" clearable placeholder="イベント・会場名・住所など" style="width:160px" />
      </el-form-item>
      <el-form-item label="都道府県">
        <el-select v-model="filters.prefecture" placeholder="すべて" style="width:120px">
          <el-option label="すべて" value="" />
          <el-option v-for="p in prefectureOptions" :key="p" :label="p" :value="p" />
        </el-select>
      </el-form-item>
      <el-form-item label="市区町村">
        <el-select v-model="filters.city_ward" placeholder="すべて" style="width:120px">
          <el-option label="すべて" value="" />
          <el-option v-for="c in cityWardOptions" :key="c" :label="c" :value="c" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">検索</el-button>
        <el-button @click="onReset">リセット</el-button>
      </el-form-item>
    </el-form>
    <el-divider />

    <!-- データテーブル -->
    <el-table :data="tournamentList" style="width: 100%" border v-loading="loading">
      <el-table-column v-for="col in columns" :key="col.prop" :prop="col.prop" :label="col.label" :sortable="col.sortable" :width="col.width || undefined">
        <template #default="scope">
          <template v-if="col.prop==='official_page'">
            <el-button size="small" type="primary" @click="openOfficial(scope.row.official_page)">公式ページへ</el-button>
          </template>
          <template v-else-if="col.prop==='rank_list'">
            <div style="white-space: pre-line">{{ formatRankList(scope.row.rank_list) }}</div>
          </template>
          <template v-else>
            <span style="white-space: pre-line">{{ scope.row[col.prop] }}</span>
          </template>
        </template>
      </el-table-column>
    </el-table>
    <!-- ページネーション -->
    <div style="margin:16px 0;text-align: right">
      <el-pagination
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        :current-page.sync="page"
        :page-size.sync="pageSize"
        :page-sizes="[10,20,50]"
        @current-change="onSearch"
        @size-change="onSearch"
        style="display: inline-block"
      />
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, watch } from 'vue'
// fetchだけでAPI通信
const API_URL = import.meta.env.VITE_API_URL
const CONFIG_API = API_URL + '/tournament/config'
const QUERY_API = API_URL + '/tournament/query'

// 列定義（全て必要な場合）
const columns = [
  { prop: 'id', label: 'ID', sortable: 'custom', width: 60 },
  { prop: 'event_id', label: 'イベントID', sortable: 'custom', width: 80 },
  { prop: 'event_name', label: 'イベント名', sortable: 'custom' },
  { prop: 'event_link', label: 'イベントリンク' },
  { prop: 'status', label: '状態' },
  { prop: 'shop_id', label: 'ショップID' },
  { prop: 'shop_name', label: 'ショップ名' },
  { prop: 'official_page', label: '公式ページ' },
  { prop: 'start_time', label: '開始日時', sortable: 'custom' },
  { prop: 'game_rule', label: 'ルール' },
  { prop: 'entry_fee', label: '参加費用', sortable: 'custom' },
  { prop: 're_entry', label: 'リ・エントリー' },
  { prop: 'prizes', label: '賞金概要' },
  { prop: 'prizes_original', label: '賞金（原文）' },
  { prop: 'address', label: '住所' },
  { prop: 'prefecture', label: '都道府県' },
  { prop: 'city_ward', label: '市区町村' },
  { prop: 'tel', label: '電話番号' },
  { prop: 'total_winners', label: '入賞者数' },
  { prop: 'total_value_jpy', label: '総賞金額' },
  { prop: 'reward_categories', label: '賞種別' },
  { prop: 'rank_list', label: '順位リスト' },
  { prop: 'reward_summary', label: '賞概要' },
  { prop: 'created_at', label: '作成日' },
  { prop: 'updated_at', label: '更新日' },
]

export default {
  setup() {
    // 状態定義
    const loading = ref(false)
    const tournamentList = ref([])
    const total = ref(0)
    const page = ref(1)
    const pageSize = ref(10)
    const prefectureOptions = ref([])
    const cityWardOptions = ref([])
    // 最初の7日デフォルト
    const today = new Date()
    const weekAgo = new Date(Date.now() - 6 * 86400 * 1000)
    const defaultRange = [weekAgo, today]
    const dateRange = ref([weekAgo, today])
    const filters = reactive({
      start_time_from: '',
      start_time_to: '',
      entry_fee_min: undefined,
      entry_fee_max: undefined,
      keyword: '',
      prefecture: '',
      city_ward: '',
      sort_field: '',
      sort_type: '',
    })
    // rank_listの表示
    function formatRankList(str) {
      try {
        const arr = JSON.parse(str)
        return arr.map(x => `${x.rank}: ${x.reward_summary}（${x.reward_value_jpy}円）`).join('\n')
      } catch { return '' }
    }
    function openOfficial(url) {
      if (url) window.open(url, '_blank')
    }
    // config取得
    async function fetchConfig() {
      const res = await fetch(CONFIG_API)
      const json = await res.json()
      prefectureOptions.value = json.data.all_prefecture || []
      cityWardOptions.value = json.data.all_city_ward || []
    }
    // メインクエリ
    async function fetchData() {
      loading.value = true
      // 日付範囲入力からパラメータ復元
      if(dateRange.value && Array.isArray(dateRange.value)){
        filters.start_time_from = dateRange.value[0] ? formatDate(dateRange.value[0]) : ''
        filters.start_time_to = dateRange.value[1] ? formatDate(dateRange.value[1]) : ''
      }
      const params = {
        ...filters,
        page: page.value,
        page_size: pageSize.value,
      }
      // パラメータnull/空文字/undefinedの除去(すべて==>不送信)
      Object.keys(params).forEach(k=>{
        if(params[k]===undefined || params[k]==='') delete params[k]
      })
      const url = QUERY_API + '?' + new URLSearchParams(params).toString()
      try {
        const res = await fetch(url)
        const json = await res.json()
        tournamentList.value = json.data || []
        total.value = json.total || (json.data ? json.data.length : 0)
      } catch {
        tournamentList.value = []
        total.value = 0
      } finally {
        loading.value = false
      }
    }
    function formatDate(dt) {
      const d = new Date(dt)
      return d.toISOString().slice(0,10)
    }
    function onSearch() {
      page.value = 1
      fetchData()
    }
    function onReset() {
      page.value = 1
      pageSize.value = 10
      filters.entry_fee_min = undefined
      filters.entry_fee_max = undefined
      filters.keyword = ''
      filters.prefecture = ''
      filters.city_ward = ''
      dateRange.value = [weekAgo, today]
      fetchData()
    }
    // 並び替え
    function handleSort({ prop, order }) {
      filters.sort_field = order ? prop : ''
      filters.sort_type = order === 'ascending' ? 'asc' : order === 'descending' ? 'desc' : ''
      fetchData()
    }
    // ページ切替
    watch([page, pageSize], fetchData)
    onMounted(()=>{
      fetchConfig()
      fetchData()
    })
    return {
      loading, tournamentList, total, page, pageSize,
      prefectureOptions, cityWardOptions, dateRange, defaultRange, filters,
      columns,
      formatRankList, openOfficial,
      onSearch, onReset,
      handleSort
    }
  }
}
</script>

<style scoped>
.el-form {
  flex-wrap: wrap;
  gap: 8px;
}
.el-table {
  margin-top: 10px;
}
@media (max-width: 700px) {
  .el-form {
    flex-direction: column;
    align-items: flex-start;
  }
  .el-table {
    font-size: 12px;
  }
}
</style>
