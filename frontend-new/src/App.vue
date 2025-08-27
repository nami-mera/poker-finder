<template>
  <div class="container">
    <!-- 上面是LOGO和标题 -->
    <div class="header">
      <img src="/poker.png" alt="Poker Logo" class="logo" />
      <h1>ポーカートーナメント検索</h1>
    </div>
    <TournamentPage />
  </div>
</template>

<script>
import TournamentPage from './components/TournamentPage.vue';
export default {
  components: { TournamentPage },
};
</script>

<style>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 16px;
  background: #fff;
}
.header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.logo {
  width: 48px;
  height: 48px;
}
</style>

