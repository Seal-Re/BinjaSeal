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
                              <i class="el-icon-house"></i>
                              <span v-if="!isCollapse">首页</span>
                          </template>
                      </el-menu-item>
                      <!-- 评估菜单 -->
                      <el-menu-item index="/evaluate">
                          <template #title>
                              <i class="el-icon-edit"></i>
                              <span v-if="!isCollapse">评估</span>
                          </template>
                      </el-menu-item>
                      <!-- 训练菜单 -->
                      <el-menu-item index="/train">
                          <template #title>
                              <i class="el-icon-document"></i>
                              <span v-if="!isCollapse">训练</span>
                          </template>
                      </el-menu-item>
                    </div>
                  </el-menu>
              </el-scrollbar>
          </div>
      </el-aside>
      <el-container>
          <el-header>
              <ToolBarLeft />
              <ToolBarRight />
          </el-header>
          <!-- 使用路由视图显示不同页面 -->
          <router-view></router-view>
      </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import ToolBarLeft from '@/layout/modules/ToolBarLeft.vue';
import ToolBarRight from '@/layout/modules/ToolBarRight.vue';

const route = useRoute();

// 直接创建一个响应式变量来控制侧边栏是否折叠
const isCollapse = ref(false);

const title = '脑卒中患者训练平台';
const activeMenu = computed(() => route.path);
</script>

<style scoped lang="scss">
@import './index.scss';

.menu-style {
  padding-top :15%;
}
</style>
