<template>
  <div class="ai-tips-page">
    <div class="page-container">
      <!-- 标题区域 -->
      <div class="header-flex">
        <h2 class="ai-tips-title">AI 建议：</h2>
      </div>
      <!-- 主要内容 -->
      <div class="main-content-container">
        <el-row class="main-content" :gutter="20">
          <!-- 建议容器 -->
          <el-col :span="18">
            <el-card v-if="aiTips.length > 0" class="tips-box common-box">
              <template #header>
                <h3 class="tips-text">AI 给出的建议如下</h3>
              </template>
              <div class="tips-content scrollable-content">
                <vue-markdown v-for="(tip, index) in aiTips" :key="index" :source="tip"></vue-markdown>
              </div>
            </el-card>
            <div v-else v-show="!isLoading">加载中...</div>
          </el-col>
          <!-- 侧边栏 -->
          <el-col :span="6">
            <el-card class="side-bar common-box">
              <!-- 侧边栏标题 -->
              <template #header>
                <div class="header-list">
                  <h3>信息</h3>
                </div>
              </template>
              <!-- 答题信息 -->
              <div class="answer-info">
                <p>用户: {{ user }}</p>
                <p v-if="userName">姓名: {{ userName }}</p> <!-- 添加姓名展示 -->
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 尾部固定区域 -->
      <div class="fixed-footer">
        <div class="footer-text">版权所有 © ???</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/index';
import router from '@/router/index';
import baseurl from '@/http/base';
import VueMarkdown from 'vue3-markdown-it';

const userStore = useUserStore();
const user = computed(() => {
  try {
    const userInfoObj = JSON.parse(userStore.userInfo);
    return userInfoObj.username || '未登录用户';
  } catch (error) {
    return '未登录用户';
  }
});
const aiTips = ref([]);
const isLoading = ref(true);
const userName = ref(''); // 用于存储用户姓名

onMounted(async () => {
  try {
    // 发送请求获取 AI 建议
    const response = await axios.get(baseurl + `/api/aiTips?username=${user.value}`);
    // 筛选出正确的建议
    if (response.data.length > 0 && response.data[0].data.length > 0) {
      const suggestion = response.data[0].data[0];
      aiTips.value = [suggestion.ai_tips];
    }

    // 发送请求获取用户信息
    const userInfoResponse = await axios.get(baseurl + `/api/userinfo_get?user=${user.value}`);
    if (userInfoResponse.data.user_info) {
      userName.value = userInfoResponse.data.user_info.name || '';
    }

    isLoading.value = false;
  } catch (error) {
    console.error('获取数据失败:', error);
    isLoading.value = false;
  }
});
</script>

<style scoped>

.ai-tips-page {
  background-color: #ffffff;
}

.ai-tips-title {
  font-size: 20px;
  font-weight: bold;
  margin-left: 30px;
}

.tips-text {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.common-box {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.tips-box {
  height: 100%;
  width: 100%;
  max-width: 100%;
  padding: 20px;
  box-sizing: border-box;
  margin-left: 30px;
}

.tips-content {
  font-size: 16px;
  line-height: 1.6;
}

.scrollable-content {
  max-height: 600px;
  overflow-y: auto;
}

.side-bar {
  height:40%;
  width:85%;
  padding: 20px;
  margin-bottom: 20px;
  margin-left:10%;
  box-sizing: border-box;
}

.answer-info {
  border-top: 1px solid #ffffff;
  padding-top: 20px;
}

.button-container {
  margin-top: 20px;
}

.big-button {
  font-size: 18px;
  padding: 20px 24px;
  width: 100%;
  height: 60px;
}

.fixed-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #ffffff;
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  color: #ffffff;
}

.footer-text {
  text-align: center;
}

.header-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height:20px;
}
</style>
