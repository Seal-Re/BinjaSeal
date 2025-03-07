<template>
  <div class="page-container">
    <!-- 头部固定区域 -->
    <div class="fixed-header">
      <div class="header-content">
        <div class="title">评估</div>
        <div class="user-info">当前登录用户：{{ user }}</div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content-container">
      <el-row class="main-content" :gutter="20">
        <!-- 题目容器 -->
        <el-col :span="18">
          <el-card v-if="questionList.length > 0" class="question-box">
            <template #header>
              <h3>{{ currentQuestion.question }}</h3>
            </template>
            <el-radio-group v-model="selectedOption" class="custom-radio-group">
              <el-radio
                v-for="(option, index) in currentQuestion.options"
                :key="index"
                :label="option"
                class="custom-radio"
              >
                {{ option }}
              </el-radio>
            </el-radio-group>
          </el-card>
          <div v-else v-show="!isLoading">加载中...</div>
        </el-col>
        <!-- 侧边栏 -->
        <el-col :span="6">
          <el-card v-if="questionList.length > 0" class="side-bar">
            <!-- 题目列表 -->
            <template #header>
              <h3>题目列表</h3>
            </template>
            <div class="question-list">
              <div
                v-for="(item, index) in questionList"
                :key="index"
                class="question-number"
                :class="{
                  'correct-answer': answerResults[index] === true,
                  'wrong-answer': answerResults[index] === false
                }"
              >
                {{ index + 1 }}
              </div>
            </div>
            <!-- 答题信息 -->
            <div class="answer-info">
              <p>答题时间：{{ getFormattedTime() }}</p>
              <p>当前得分：{{ score }}</p>
            </div>
          </el-card>
          <div v-else v-show="!isLoading">加载中...</div>
          <!-- 按钮容器，移到侧边栏卡片外部 -->
          <el-row v-if="questionList.length > 0" class="button-container" justify="center">
            <el-col>
              <el-button
                type="primary"
                :disabled="false"
                @click="currentIndex === questionList.length - 1? submitAnswers() : nextQuestion()"
                class="big-button"
              >
                {{ currentIndex === questionList.length - 1? '提交' : '下一题' }}
              </el-button>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>

    <!-- 尾部固定区域 -->
    <div class="fixed-footer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/userStore';
import router from '@/router/index';

const userStore = useUserStore();
// 登录用户
const user = computed(() => userStore.userInfo?.username || '未登录用户');
// 题目列表
const questionList = ref([]);
// 当前题目索引
const currentIndex = ref(0);
// 当前题目
const currentQuestion = computed(() => questionList.value[currentIndex.value]);
// 选择的选项
const selectedOption = ref('');
// 答题开始时间
const startTime = ref(new Date());
// 得分
const score = ref(0);
// 记录每道题的作答情况
const answerRecords = ref([]);
// 记录每道题的作答结果（正确或错误）
const answerResults = ref([]);
// 加载状态
const isLoading = ref(true);

// 获取格式化后的答题时间
const getFormattedTime = () => {
  const now = new Date();
  const diff = now - startTime.value;
  const minutes = Math.floor(diff / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
};

// 下一题
const nextQuestion = () => {
  if (currentIndex.value < questionList.value.length - 1) {
    // 记录当前题目的作答情况
    answerRecords.value[currentIndex.value] = selectedOption.value;
    // 判断答案并计算得分
    const currentAnswer = currentQuestion.value.answer;
    const currentScore = currentQuestion.value.score;
    const isCorrect = selectedOption.value === currentAnswer;
    if (isCorrect) {
      score.value += currentScore;
    }
    // 记录作答结果
    answerResults.value[currentIndex.value] = isCorrect;
    currentIndex.value++;
    // 恢复当前题目的作答记录
    selectedOption.value = answerRecords.value[currentIndex.value];
  }
};

// 提交答案
const submitAnswers = async () => {
  // 记录最后一题的作答情况
  answerRecords.value[currentIndex.value] = selectedOption.value;
  // 判断最后一题答案并计算得分
  const currentAnswer = currentQuestion.value.answer;
  const currentScore = currentQuestion.value.score;
  const isCorrect = selectedOption.value === currentAnswer;
  if (isCorrect) {
    score.value += currentScore;
  }
  // 记录最后一题作答结果
  answerResults.value[currentIndex.value] = isCorrect;


  try {
    // 构造符合后端格式的数据
    const submissionData = {
      user: user.value,
      data: [
        {
          answerRecords: answerRecords.value,
          answerResults: answerResults.value,
          score: score.value,
          date: new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
        }
      ]
    };

    // 发送数据到后端
    const response = await axios.post('http://localhost:5000/api/submit', submissionData);

    console.log('答案提交成功:', response.data);
  } catch (error) {
    console.error('答案提交失败:', error);
  }

  // 这里可以添加提交答案后的逻辑，比如将结果发送到后端等
  console.log('答案已提交，最终得分：', score.value);
  router.push("/exchange");
};

onMounted(async () => {
  try {
    // 发送请求获取题目数据
    const response = await axios.get('http://localhost:5000/api/questions');
    questionList.value = response.data;
    // 初始化作答记录和结果数组
    answerRecords.value = Array(questionList.value.length).fill('');
    answerResults.value = Array(questionList.value.length).fill(null);
    isLoading.value = false;
  } catch (error) {
    console.error('获取题目数据失败:', error);
    isLoading.value = false;
  }
});
</script>

<style scoped>
/* 样式部分保持不变 */
html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px; /* 头部高度 */
  background-color: #fafafa;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100; /* 确保头部显示在最上层 */
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.user-info {
  font-size: 16px;
  color: #666;
}

.main-content-container {
  flex: 1;
  padding: 100px 20px 20px; /* 为了避免内容被头部遮挡，设置顶部内边距 */
}

.evaluation-container {
  padding: 20px;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.main-content {
  /* 如果不需要额外样式，可以直接删除这个选择器及其规则集 */
  /* 或者添加一些有意义的样式，例如： */
  margin-bottom: 20px; /* 这里添加了一个示例样式，你可以根据需求修改 */
}

.question-box {
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 300px; /* 保证卡片有足够高度 */
}

.side-bar {
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px; /* 为按钮留出空隙 */
}

.question-list {
  margin-bottom: 20px;
}

.question-number {
  cursor: pointer;
  margin: 5px;
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 50%;
  transition: all 0.3s;
}

.question-number:hover {
  background-color: #f0f0f0;
}

.answer-info {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.button-container {
  margin-top: 20px;
}

.big-button {
  font-size: 18px; /* 增大字体大小 */
  padding: 20px 24px; /* 增大上下内边距以放大高度 */
  width: 100%; /* 使按钮宽度填满父容器 */
  height: 60px;
}

.custom-radio-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
  gap: 20px; /* 选项间距 */
}

.custom-radio {
  width: 80%; /* 控制选项宽度 */
  margin: 0 !important; /* 清除默认边距 */
  padding: 15px 20px;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.custom-radio:hover {
  background-color: #f5f7fa;
}

.custom-radio .el-radio__input {
  margin-right: 12px;
}

.custom-radio .el-radio__label {
  font-size: 16px;
  vertical-align: middle;
}

/* 正确答案样式 */
.correct-answer {
  background-color: green;
  color: white;
}

/* 错误答案样式 */
.wrong-answer {
  background-color: red;
  color: white;
}

.fixed-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px; /* 尾部高度 */
  background-color: #ffffff;
  z-index: 100; /* 确保尾部显示在最上层 */
}
</style>
