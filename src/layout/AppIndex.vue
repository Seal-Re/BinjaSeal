<template>
  <el-container class="layout">
    <el-aside>
      <!-- 直接使用一个响应式变量来控制侧边栏宽度 -->
      <div class="aside-box" :style="{ width: isCollapse ? '65px' : '300px' }">
        <div class="logo flx-center">
          <img class="logo-img" src="@/assets/icons/logo.svg" alt="logo" />
          <span v-show="!isCollapse" class="logo-text">{{ title }}</span>
        </div>
        <el-scrollbar>
          <el-menu :default-active="activeMenu" :router="true" :unique-opened="true" :collapse-transition="false" :collapse="isCollapse">
            <div class="menu-style">
              <!-- 首页菜单 -->
              <el-menu-item index="/home">
                <template #title>
                  <img v-if="!isCollapse" class="menu-icon" src="@/assets/icons/home.svg" alt="home icon" />
                  <i v-else class="el-icon-house"></i>
                  <span v-if="!isCollapse">首页</span>
                </template>
              </el-menu-item>
              <!-- 评估菜单 -->
              <el-menu-item index="/evaluate">
                <template #title>
                  <img v-if="!isCollapse" class="menu-icon" src="@/assets/icons/evaluate.svg" alt="evaluate icon" />
                  <i v-else class="el-icon-edit"></i>
                  <span v-if="!isCollapse">认知评估</span>
                </template>
              </el-menu-item>
              <!-- 训练菜单 -->
              <el-menu-item index="/train">
                <template #title>
                  <img v-if="!isCollapse" class="menu-icon" src="@/assets/icons/train.svg" alt="train icon" />
                  <i v-else class="el-icon-document"></i>
                  <span v-if="!isCollapse">认知训练</span>
                </template>
              </el-menu-item>
              <!-- 训练菜单 -->
              <el-menu-item index="/aiTips">
                <template #title>
                  <img v-if="!isCollapse" class="menu-icon" src="@/assets/icons/AITips.svg" alt="AITips icon" />
                  <i v-else class="el-icon-document"></i>
                  <span v-if="!isCollapse">AI建议</span>
                </template>
              </el-menu-item>
            </div>
          </el-menu>
        </el-scrollbar>
      </div>
    </el-aside>
    <el-container>
      <el-header>
        <div class="breadcrumb">
          <span v-for="(item, index) in breadcrumbList" :key="index">
            <router-link :to="item.path">{{ item.name }}</router-link>
            <span v-if="index < breadcrumbList.length - 1">/</span>
          </span>
        </div>
        <ToolBarRight />
      </el-header>
      <!-- 使用路由视图显示不同页面 -->
      <router-view></router-view>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ToolBarLeft from '@/layout/modules/ToolBarLeft.vue';
import ToolBarRight from '@/layout/modules/ToolBarRight.vue';
import { useBreadCrumb } from "@/store/index";

const route = useRoute();
const breadcrumbStore = useBreadCrumb();

// 直接创建一个响应式变量来控制侧边栏是否折叠
const isCollapse = ref(false);

const title = '脑卒中认知康复系统';
const activeMenu = computed(() => route.path);

// 定义菜单数据
const menuList = [
  {
    path: '/home',
    name: '首页'
  },
  {
    path: '/evaluate',
    name: '认知评估'
  },
  {
    path: '/train',
    name: '认知训练'
  },
  {
    path: '/aiTips',
    name: 'AI建议'
  },
  {
    path: '/userinfo',
    name: '用户信息'
  }
];

// 初始化菜单数据
onMounted(() => {
  breadcrumbStore.getMenuList(menuList);
});

// 获取当前路径的面包屑列表
const breadcrumbList = computed(() => {
  return breadcrumbStore.breadcrumbListGet(route.path) || [];
});
</script>

<style scoped lang="scss">
@import './index.scss';

// 自定义菜单样式
.menu-style {
  .el-menu-item {
    // 正常状态样式
    background-color: #f4f4f4;
    color: #333;
    border-radius: 4px;
    margin: 8px;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #e0e0e0;
    }

    // 激活状态样式
    &.is-active {
      background-color: #007bff;
      color: #fff;

      i {
        color: #fff;
      }

      .menu-icon {
        filter: brightness(0) invert(1); // 让激活状态下图标颜色变白
      }
    }
  }

  .menu-icon {
    width: 20px;
    height: 20px;
    margin-right: 8px;
    vertical-align: middle;
  }
}

.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.breadcrumb {
  display: flex;
  align-items: center;
  margin-left: 20px;
  a {
    color: var(--el-header-text-color);
    margin-right: 5px;
  }
  span {
    margin-right: 5px;
  }
  order: -1; // 将面包屑区域置于最左边
}
</style>
