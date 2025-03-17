<template>
  <!-- 模板代码保持不变 -->
  <div v-if="Flag === 0">
    <div class="page-container">
      <!-- 新增用户评估区域 -->
      <el-card class="patient-summary">
        <template #header>
          <div class="header-flex">
            <h2 class="patieny-summary-title">用户评估：</h2>
          </div>
        </template>
        <!-- 主要内容 -->
        <div class="main-content-container">
          <el-row class="main-content" :gutter="20">
            <!-- 题目容器 -->
            <el-col :span="18">
              <el-card v-if="questionList.length > 0" class="question-box">
                <template #header>
                  <h3 class="question-text">{{ currentQuestion.question }}</h3>
                </template>
                <!-- 根据 model 参数判断渲染选择题还是填空题 -->
                <template v-if="currentQuestion.model === '0'">
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
                </template>
                <template v-else-if="currentQuestion.model === '1'">
                  <el-input v-model="selectedOption" placeholder="请输入答案"></el-input>
                </template>
                <!-- 新增图片选择题 -->
                <template v-else-if="currentQuestion.model === '2'">
                  <el-radio-group v-model="selectedOption" class="image-radio-group">
                    <el-row :gutter="20" class="image-options-container">
                      <el-col
                        v-for="(option, index) in currentQuestion.options"
                        :key="index"
                        :span="12"
                        class="image-option-col"
                      >
                        <el-radio :label="option" class="image-radio-item">
                          <div class="image-wrapper">
                            <img
                              :src="baseurl+`/images_data/?name=${option}`"
                              alt="选项图片"
                              class="option-image"
                            >
                          </div>
                        </el-radio>
                      </el-col>
                    </el-row>
                  </el-radio-group>
                </template>
              </el-card>
              <div v-else v-show="!isLoading">加载中...</div>
            </el-col>
            <!-- 侧边栏 -->
            <el-col :span="6">
              <el-card v-if="questionList.length > 0" class="side-bar">
                <!-- 题目列表 -->
                <template #header>
                  <div class="header-list">
                    <h3>题目列表</h3>
                  </div>
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
      </el-card>

      <!-- 尾部固定区域 -->
      <div class="fixed-footer"></div>
    </div>
  </div>
  <div v-else>
    <div class="page-container result-page">
      <!-- 主要内容区域，显示得分和操作按钮 -->
      <div class="main-content-container result-main-content">
        <div class="result-box">
          <!-- 显示得分 -->
          <h1 class="score-text">{{ score_view }}分</h1>
          <!-- 查看题目详情按钮 -->
          <el-button type="primary" class="result-button" @click="showQuestionDetails">
            查看题目详情
          </el-button>
          <!-- 返回主页按钮 -->
          <el-button type="primary" class="result-button" @click="goBackHome">
            返回主页
          </el-button>
        </div>
      </div>

      <!-- 尾部固定区域，显示版权信息 -->
      <div class="fixed-footer">
        <div class="footer-text">版权所有 © ???</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/userStore';
import router from '@/router/index';
import baseurl from '@/http/base';

const userStore = useUserStore();
// 登录用户
const user = computed(() => userStore.userInfo?.username || '未登录用户');
// 题目列表
const questionList = ref([]);
// 当前题目索引
const currentIndex = ref(0);
// 当前题目
const currentQuestion = computed(() => questionList.value[currentIndex.value]);
// 选择的选项或输入的答案
const selectedOption = ref('');
// 答题开始时间
const startTime = ref(new Date());
// 得分
const score = ref(0);
const score_view = ref(0);
// 记录每道题的作答情况
const answerRecords = ref([]);
// 记录每道题的作答结果（正确或错误）
const answerResults = ref([]);
// 加载状态
const isLoading = ref(true);

const Flag = ref(0);

// 查看题目详情方法，可按需实现具体逻辑
const showQuestionDetails = () => {
  console.log('查看题目详情逻辑');
};

// 返回主页方法
const goBackHome = () => {
  router.push('/home');
};

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
  if (questionList.value.length > 0 && currentIndex.value < questionList.value.length - 1) {
    // 记录当前题目的作答情况
    answerRecords.value[currentIndex.value] = selectedOption.value;
    // 判断答案并计算得分
    const currentAnswer = currentQuestion.value.answer;
    const currentScore = parseInt(currentQuestion.value.score, 10); // 将 score 转换为数字
    const isCorrect = selectedOption.value === currentAnswer;
    if (isCorrect) {
      score.value += currentScore;
    }
    // 记录作答结果
    answerResults.value[currentIndex.value] = isCorrect;
    currentIndex.value++;
    // 恢复当前题目的作答记录
    selectedOption.value = answerRecords.value[currentIndex.value] || '';
  }
};

const submitAnswers = async () => {
  if (questionList.value.length > 0) {
    // 记录最后一题的作答情况
    answerRecords.value[currentIndex.value] = selectedOption.value;
    // 判断最后一题答案并计算得分
    const currentAnswer = currentQuestion.value.answer;
    const currentScore = parseInt(currentQuestion.value.score, 10); // 将 score 转换为数字
    const isCorrect = selectedOption.value === currentAnswer;
    if (isCorrect) {
      score.value += currentScore;
    }
    // 记录最后一题作答结果
    answerResults.value[currentIndex.value] = isCorrect;

    try {
      // 构建训练数据
      const trainingData = {
        "失算症训练": { "data": [] },
        "思维障碍训练": { "data": [] },
        "注意障碍训练": { "data": [] },
        "知觉障碍训练": { "data": [] },
        "记忆障碍训练": { "data": [] }
      };

      // 填充训练数据
      for (let i = 0; i < questionList.value.length; i++) {
        const question = questionList.value[i];
        const type = question.class;
        const value = answerResults.value[i]? question.score : 0;
        trainingData[type].data.push({
          id: i + 1,
          value: value.toString(),
          date: new Date().toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          })
        });
      }

      // 构建提交数据
      const submissionData = {
        user: user.value,
        data: [
          {
            answerRecords: answerRecords.value,
            answerResults: answerResults.value,
            score: score.value,
            date: new Date().toLocaleString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit'
            })
          }
        ],
        trainingData: trainingData  // 添加训练数据字段
      };

      // 只发送一次请求
      axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';
      const response = await axios.post(baseurl+'/api/submit', submissionData);
      console.log('数据提交成功:', response.data);
    } catch (error) {
      console.error('答案提交失败:', error);
    }
    score_view.value = score.value;
    score.value = 0;
    Flag.value = 1;
  }
};

onMounted(async () => {
  // 获取 html 元素
  const htmlElement = document.documentElement;
  // 设置 lang 属性
  htmlElement.lang = 'zh';
  // 设置样式
  htmlElement.style.height = '95%';

  try {
    // 发送请求获取题目数据
    const response = await axios.get(baseurl+'/api/questions');
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
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.page-container {
  display: flex;
  flex-direction: column;
  height: 95vh; /* 使用视口高度 */
  width: 100%; /* 修改为 100%，确保不溢出 */
  overflow-x: hidden; /* 防止水平溢出 */
}

.main-content {
  width: 100%;
  max-width: 100%;
}

.main-content-container {
  flex: 1;
  padding: 30px 20px 80px; /* 减少顶部 padding，增加底部 padding */
  margin-right: 0; /* 修改为 0，避免额外的右边距 */
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 顶部对齐 */
  overflow-x: hidden; /* 防止水平溢出 */
}

.question-box {
  height: 100%;
  width: 100%;
  max-width: 100%;
  padding: 20px;
  box-sizing: border-box;
  margin-left: 0;
}

.side-bar {
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.question-list {
  margin-bottom: 20px;
  height: 105px;
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
  height: 60px; /* 尾部高度 */
  background-color: #f9f9f9;
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  color: #888;
}

.footer-text {
  text-align: center;
}

/* 页面二样式 */
.result-page {
  background-color: transparent; /* 修改为透明背景 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  margin-right: 0; /* 修改为 0，避免额外的右边距 */
}

.result-box {
  background-color: #fff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  padding: 60px 40px;
  text-align: center;
  box-sizing: border-box;
}

.score-text {
  font-size: 60px;
  font-weight: 700;
  color: #3498db;
  margin-bottom: 40px;
}

.result-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 240px;
  height: 50px;
  margin: 20px auto;
  font-size: 18px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.result-button:hover {
  background-color: #2980b9;
}

/* 图片选择题布局修复 */
.image-radio-group {
  width: 100%; /* 修改为 100%，确保自适应 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 居中显示 */
  gap: 5px; /* 图片之间的间距 */
}

.image-options-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 居中显示 */
  gap: 16px; /* 图片之间的间距 */
  max-width: 100%; /* 修改为 100%，确保自适应 */
  margin: 0 auto; /* 居中 */
}

.image-option-col {
  flex: 0 0 calc(50% - 8px); /* 两列布局，减去间距 */
  max-width: calc(50% - 8px); /* 限制最大宽度 */
  box-sizing: border-box;
}

.image-radio-item {
  width: 100%;
  height: 90%;
}

.image-wrapper {
  width: 45%;
  aspect-ratio: 1 / 1; /* 保持1:1宽高比 */
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9; /* 添加背景色 */
}

.option-image {
  max-width: 90%; /* 限制最大宽度 */
  max-height: 60%; /* 限制最大高度 */
  object-fit: contain; /* 保持图片比例 */
  transition: transform 0.3s;
}

.image-radio-item.is-checked .image-wrapper {
  border-color: #409eff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

/* 修复Element Plus radio样式覆盖 */
:deep(.el-radio__input) {
  position: absolute;
  top: 40%;
  left: 1%;
}

:deep(.el-radio__label) {
  width: 100%;
  padding: 5 !important;
}

/* 患者情况概况和用户评估区域样式 */
.patient-summary {
  margin-top: 2.7%;
  margin-bottom: 6.75%;
  margin-left: 2.3%;
  margin-right: 2%; /* 修改为 2%，避免过大的右边距 */
  position: relative;
  z-index: 1;
}

.header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 20pt;
}

.header-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 20pt;
}

.patieny-summary-title {
  font-size: 20px;
  font-weight: bold;
}

.question-text {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content-container {
    flex-direction: column;
  }
  .el-col {
    width: 100%;
  }
}
</style>
