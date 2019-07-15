<template>
  <div class="dashboard-container">
    <span>{{ username }}, 欢迎来到环球自动化测试平台</span>
  </div>
</template>

<script>

export default {
  name: 'dashboard',
  data() {
    return {
      // username: localStorage.getItem("username")
      username: 'admin'
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
