<template>
  <div class="home-page">
    <!-- 顶部白条区域 -->
    <div class="top-white-bar">
      <!-- 修改后的头部容器 -->
      <div class="header-content">
        <div class="title">脑卒中患者训练平台</div>
        <div class="user-info-container">
          <div class="user-info">当前登录用户：{{ user }}</div>
          <el-button type="primary" @click="logout">登出</el-button>
        </div>
      </div>
    </div>

    <!-- 新增的背景空白区域 -->
    <div class="summary-top-space"></div>

    <!-- 患者情况概况区域 -->
    <el-card class="patient-summary">
      <template #header>
        <h2>患者情况概况：</h2>
      </template>
      <div class="training-container">
        <div
          v-for="(training, index) in Object.values(chartData)"
          :key="index"
          class="training-item"
        >
          <h3 class="training-name">{{ training.name }}</h3>
          <div class="info-box">
            <div
              v-for="item in sortedData(training.data)"
              :key="item.id"
              class="data-item"
            >
              <p>日期：{{ item.date }}</p>
              <p>值：{{ item.value }}</p>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 新增的透明块 -->
    <div class="separate-space"></div>

    <!-- 答题情况滚动框区域 -->
    <el-card class="answer-scroll-container">
      <template #header>
        <h2>答题情况：</h2>
      </template>
      <!-- 添加判断，如果没有答题记录则显示“暂无答题记录” -->
      <div v-if="answerList.length === 0" class="no-answer-message">暂无答题记录</div>
      <div v-else>
        <div v-for="(answerItem, index) in answerList" :key="index" class="answer-item">
          <div>答题时间：{{ answerItem.date }}</div>
          <div>答题分数：{{ answerItem.score }}</div>
          <el-button type="text" size="small">查看分析报告</el-button>
        </div>
      </div>
    </el-card>

    <!-- 评估和训练按钮区域 -->
    <el-row :gutter="20" class="action-buttons">
      <el-col :span="12">
        <el-button type="primary" class="btn" style="height: 100px; font-size: 28px;" @click="handleEvaluate">评估</el-button>
      </el-col>
      <el-col :span="12">
        <el-button type="primary" class="btn" style="height: 100px; font-size: 28px;" @click="handleTrain">训练</el-button>
      </el-col>
    </el-row>

    <!-- 底部白条区域 -->
    <div class="bottom-white-bar"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/userStore';
import router from '@/router/index';
import axios from 'axios';

const userStore = useUserStore();
// 登录用户
const user = computed(() => userStore.userInfo?.username || '未登录用户');

const chartData = ref({});
const answerList = ref([]);

// 定义一个计算属性来对数据进行时间倒序排序
const sortedData = computed(() => {
  return (data) => {
    return [...data].sort((a, b) => {
      return new Date(b.date) - new Date(a.date);
    });
  };
});

const logout = () => {
  console.log('用户登出');
  userStore.logout();
  router.push('/login');
};

// 点击评估按钮的处理方法
const handleEvaluate = () => {
  console.log('点击了评估按钮');
  router.push('/evaluate');
};

// 点击训练按钮的处理方法
const handleTrain = () => {
  console.log('点击了训练按钮');
  router.push('/train');
};

onMounted(async () => {
  try {
    const chartResponse = await axios.get('http://localhost:5000/api/chartData');
    chartData.value = chartResponse.data;

    // 获取当前登录用户的答题记录
    const answerResponse = await axios.get(`http://localhost:5000/api/userAnswers?username=${user.value}`);
    answerList.value = answerResponse.data;
  } catch (error) {
    console.error('获取数据失败:', error);
  }
});
</script>

<style scoped>
/* 样式代码保持不变 */
.home-page {
  padding: 0 20px;
  position: relative;
  overflow-x: hidden;
}

.top-white-bar {
  background-color: white;
  padding: 20px 0;
  /* 修改定位方式 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  /* 新增阴影增强层次感 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.summary-top-space {
  height: 10px; /* 根据实际需要调整高度 */
  background-color: transparent;
  margin-top: 80px; /* 与顶部固定栏保持间距 */
}

.bottom-white-bar {
  background-color: white;
  height: 50px;
  width: 100%; /* 修改为100% */
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 100; /* 设置层级，避免遮挡其他内容 */
}

.header-container {
  margin-bottom: 0;
  width: 100%;
  max-width: 1200px; /* 可以根据需要调整最大宽度 */
  margin: 0 auto; /* 水平居中 */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 24px;
  font-weight: bold;
}

.user-info-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  font-size: 16px;
}

.patient-summary {
  margin-top: 20px; /* 减少原有间距 */
  position: relative;
  z-index: 1;
}

.info-box {
  border: 1px solid #e4e7ed;
  padding: 10px;
  height: 300px;
  box-sizing: border-box;
  overflow-y: auto;
}

.data-item {
  border: 1px solid #ccc;
  padding: 8px;
  margin-bottom: 8px;
}

.training-name {
  text-align: center;
  margin-bottom: 5px;
  font-size: 18px;
  font-weight: bold;
}

.answer-scroll-container {
  height: 300px;
  overflow-y: scroll;
  margin-bottom: 20px;
}

.answer-item {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 80px; /* 调整下边距，避免被底部白条遮挡 */
}

.btn {
  width: 100%;
}

.training-container {
  display: flex;
  gap: 15px; /* 控制间距 */
  flex-wrap: wrap;
}

.training-item {
  flex: 1;
  min-width: calc(20% - 12px); /* 5个项目，考虑间距 */
  box-sizing: border-box;
}

/* 新增的透明块样式 */
.separate-space {
  height: 20px; /* 可以根据需要调整高度 */
  background-color: transparent;
}

/* 响应式调整 */
@media (max-width: 1200px) {
 .training-item {
    min-width: calc(25% - 12px); /* 4列 */
  }
}

@media (max-width: 992px) {
 .training-item {
    min-width: calc(33.33% - 12px); /* 3列 */
  }
}

@media (max-width: 768px) {
 .training-item {
    min-width: calc(50% - 12px); /* 2列 */
  }
}

@media (max-width: 480px) {
 .training-item {
    min-width: 100%; /* 1列 */
  }
}

@media screen and (max-width: 768px) {
 .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

 .user-info-container {
    margin-top: 10px;
  }
}

/* 新增的暂无答题记录样式 */
.no-answer-message {
  text-align: center;
  color: #666;
  padding: 10px;
}
</style>
