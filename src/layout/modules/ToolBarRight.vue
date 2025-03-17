<template>
  <div class="tool-bar-ri">
      <!-- <div class="header-icon">
          <Message />
      </div> -->
      <span class="username">{{ user }}</span>
      <Avatar />
  </div>
</template>

<script lang="ts" setup>
import { ref,computed } from 'vue';
// import Message from '@/components/Message.vue';
import Avatar from '@/components/AppAvatar.vue';
import { useUserStore } from "@/stores/userStore";

// 手动管理用户信息，这里假设一个默认的用户名
const userStore = useUserStore();
const user = computed(() => (userStore.userInfo as { username: string }).username || '未登录用户');
// 如果有获取用户信息的接口调用，可以在这里模拟
// 例如：
// setTimeout(() => {
//     username.value = '实际用户名';
// }, 1000);

</script>

<style scoped lang="scss">
.tool-bar-ri {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-right: 25px;
  .header-icon {
      display: flex;
      align-items: center;
      margin-top: 8px;
  }
  .username {
      margin: 0 20px;
      font-size: 15px;
      color: var(--el-header-text-color);
  }
}
</style>
