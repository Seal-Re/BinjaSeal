<template>
  <!-- 模板代码保持不变 -->
  <div class="home-page">
    <!-- 顶部白条区域 -->
    <div class="top-white-bar">
      <!-- 修改后的头部容器 -->
      <div class="header-content">
        <!-- 添加图标 -->
        <div class="title-container">
          <img src="@/assets/rzkh.svg" alt="图标" class="title-icon">
          <div class="title">脑卒中患者训练平台</div>
        </div>
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
        <div class="header-flex">
          <h2>患者情况概况：</h2>
          <el-date-picker
            v-model="selectedDate"
            type="date"
            placeholder="选择日期"
            @change="filterTableData"
          ></el-date-picker>
        </div>
      </template>
      <!-- 折线图和饼状图容器 -->
      <div class="chart-container">
        <div ref="lineChartRef" class="line-chart"></div>
        <div ref="pieChartRef" class="pie-chart"></div>
      </div>
      <!-- 表格部分 -->
      <el-table :data="filteredTableData" stripe>
        <el-table-column prop="date" label="时间"></el-table-column>
        <el-table-column prop="id" label="id"></el-table-column>
        <el-table-column prop="失算症训练" label="失算症训练"></el-table-column>
        <el-table-column prop="思维障碍训练" label="思维障碍训练"></el-table-column>
        <el-table-column prop="注意障碍训练" label="注意障碍训练"></el-table-column>
        <el-table-column prop="知觉障碍训练" label="知觉障碍训练"></el-table-column>
        <el-table-column prop="记忆障碍训练" label="记忆障碍训练"></el-table-column>
        <el-table-column prop="totalScore" label="总分"></el-table-column>
      </el-table>
    </el-card>

    <!-- 新增的透明块 -->
    <div class="separate-space"></div>

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
import { ref, computed, onMounted, watch } from 'vue';
import { useUserStore } from '@/stores/userStore';
import router from '@/router/index';
import axios from 'axios';
import { format } from 'date-fns';
import * as echarts from 'echarts';
import baseurl from '@/http/base';

const userStore = useUserStore();
// 登录用户
const user = computed(() => userStore.userInfo?.username || '未登录用户');

const tableData = ref([]);
const selectedDate = ref(null);
const lineChartRef = ref(null);
const pieChartRef = ref(null);

// 定义一个函数将日期格式从 2025/3/1 转换为 2025 - 03 - 01
const convertDate = (dateStr) => {
  // 分离日期和时间部分（处理两种格式：有时间和无时间）
  const [datePart] = dateStr.split(' '); // 分割日期和时间部分
  const [year, month, day] = datePart.split(/[/-]/); // 处理不同分隔符
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
};

const filteredTableData = computed(() => {
  if (!selectedDate.value) {
    return tableData.value;
  }
  const formattedDate = format(selectedDate.value, 'yyyy-MM-dd');

  return tableData.value.filter(item => {
    // 统一转换item.date格式
    const itemDate = convertDate(item.date);
    return itemDate === formattedDate;
  });
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

const filterTableData = () => {
  // 日期选择改变时，会自动触发 filteredTableData 的计算属性更新
  drawCharts();
};

const drawCharts = () => {
  const dataToUse = selectedDate.value? filteredTableData.value : tableData.value; // 根据是否选择日期决定使用的数据
  const dateMap = new Map();
  const moduleScores = {
    '失算症训练': [],
    '思维障碍训练': [],
    '注意障碍训练': [],
    '知觉障碍训练': [],
    '记忆障碍训练': [],
    'totalScore': []
  };
  const moduleTotalScores = {
    '失算症训练': 0,
    '思维障碍训练': 0,
    '注意障碍训练': 0,
    '知觉障碍训练': 0,
    '记忆障碍训练': 0,
    'totalScore': 0
  };

  dataToUse.forEach(item => {
    const date = convertDate(item.date);
    if (!dateMap.has(date)) {
      dateMap.set(date, {
        '失算症训练': [],
        '思维障碍训练': [],
        '注意障碍训练': [],
        '知觉障碍训练': [],
        '记忆障碍训练': [],
        'totalScore': []
      });
    }
    Object.keys(moduleScores).forEach(module => {
      dateMap.get(date)[module].push(item[module]);
      moduleTotalScores[module] += item[module];
    });
  });

  const dates = Array.from(dateMap.keys()).sort();
  dates.forEach(date => {
    Object.keys(moduleScores).forEach(module => {
      const scores = dateMap.get(date)[module];
      const average = scores.reduce((sum, score) => sum + score, 0) / scores.length;
      moduleScores[module].push(average);
    });
  });

  // 绘制折线图
  const lineChart = echarts.init(lineChartRef.value);
  const selectedDateStr = selectedDate.value? format(selectedDate.value, 'yyyy-MM-dd') : null;
  const lineOption = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: {
      type: 'value'
    },
    series: Object.keys(moduleScores).map(module => ({
      name: module,
      type: 'line',
      data: moduleScores[module],
      markPoint: {
        data: selectedDateStr && dates.includes(selectedDateStr)? [
          {
            coord: [selectedDateStr, moduleScores[module][dates.indexOf(selectedDateStr)]],
            itemStyle: {
              color: 'red'
            }
          }
        ] : []
      }
    }))
  };
  lineChart.setOption(lineOption);

  // 绘制饼状图
  const pieChart = echarts.init(pieChartRef.value);
  const pieData = Object.keys(moduleTotalScores).filter(module => module!== 'totalScore').map(module => ({
    value: moduleTotalScores[module],
    name: module
  }));
  const pieOption = {
    tooltip: {
      trigger: 'item'
    },
    series: [
      {
        name: '模块得分占比',
        type: 'pie',
        radius: '50%',
        data: pieData
      }
    ]
  };
  pieChart.setOption(pieOption);
};

onMounted(async () => {
  try {
    const response = await axios.get(baseurl+`/api/deliverScoreData?username=${user.value}`);
    const data = response.data.data; // 先获取 "data" 键对应的值

    // 创建对象来按日期和id分组存储数据
    const recordsMap = new Map();

    // 遍历所有训练类型
    for (const trainingType in data) {
      // 遍历每个训练类型的数据项
      for (const item of data[trainingType]) { // 注意这里不需要再访问.data
        // 创建唯一标识键（日期 + id）
        const key = `${item.date}-${item.id}`;

        // 如果不存在则初始化记录
        if (!recordsMap.has(key)) {
          recordsMap.set(key, {
            date: item.date,
            id: item.id,
            失算症训练: 0,
            思维障碍训练: 0,
            注意障碍训练: 0,
            知觉障碍训练: 0,
            记忆障碍训练: 0,
            totalScore: 0
          });
        }

        // 获取当前记录
        const record = recordsMap.get(key);

        // 将当前训练类型的值转换为数字（处理无效值为0）
        const numericValue = Number(item.value) || 0;

        // 更新对应训练类型的值和总分
        record[trainingType] = numericValue;
        record.totalScore += numericValue;
      }
    }

    // 将Map转换为数组并排序
    const allRows = Array.from(recordsMap.values()).sort((a, b) => {
      const dateA = new Date(convertDate(a.date));
      const dateB = new Date(convertDate(b.date));
      return dateB - dateA || b.id - a.id;
    });

    tableData.value = allRows;



    drawCharts(); // 初始加载时绘制图表
  } catch (error) {
    console.error('获取数据失败:', error);
  }
});

watch(selectedDate, () => {
  drawCharts();
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
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 100%; /* 修改为100%以占满宽度 */
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px; /* 设置与边缘的间隔 */
  box-sizing: border-box; /* 确保内边距包含在宽度内 */
}

.title-container {
  display: flex;
  align-items: center;
}

.title-icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.summary-top-space {
  height: 10px;
  background-color: transparent;
  margin-top: 80px;
}

.bottom-white-bar {
  background-color: white;
  height: 50px;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 100;
}

.header-container {
  margin-bottom: 0;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
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
  margin-top: 5px;
  margin-bottom: 5px;
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

.action-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 80px;
}

.btn {
  width: 100%;
}

.training-container {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.training-item {
  flex: 1;
  min-width: calc(20% - 12px);
  box-sizing: border-box;
}

.separate-space {
  height: 20px;
  background-color: transparent;
}

/* 响应式调整 */
@media (max-width: 1200px) {
 .training-item {
    min-width: calc(25% - 12px);
  }
}

@media (max-width: 992px) {
 .training-item {
    min-width: calc(33.33% - 12px);
  }
}

@media (max-width: 768px) {
 .training-item {
    min-width: calc(50% - 12px);
  }
}

@media (max-width: 480px) {
 .training-item {
    min-width: 100%;
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

.header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 新增图表容器样式 */
.chart-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.line-chart {
  width: 60%;
  height: 300px;
}

.pie-chart {
  width: 35%;
  height: 300px;
}
</style>
