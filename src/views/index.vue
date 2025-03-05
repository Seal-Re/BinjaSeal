<template>
  <div class="login-wrapper">
    <div class="log_in">
      <div class="title">登入</div>

      <div class="log_IO">
        <el-input
          v-model="username"
          style="width: 240px"
          placeholder="请输入您的用户名"
          clearable
          :class="{ 'is-invalid': isUsernameInvalid }"
        />
        <p v-if="isUsernameInvalid" class="invalid-feedback">用户名不能为空</p>
        <el-input
          v-model="password"
          style="width: 240px"
          type="password"
          placeholder="请输入您的密码"
          show-password
          :class="{ 'is-invalid': isPasswordInvalid }"
        />
        <p v-if="isPasswordInvalid" class="invalid-feedback">密码不能为空</p>
        <el-button
          @click="handleLogin"
          type="primary"
          round
          :class="
          [
            isLoginFailed === 0 ? 'status-blue' : '',
            isLoginFailed === 1 ? 'status-green' : '',
            isLoginFailed === 2 ? 'status-red' : ''
          ]"
        >
          登入
        </el-button>

      </div>
      <p v-if="!loginResult" style="height: 25px;"></p>
      <p v-if="loginResult">{{ loginResult }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, ElMessage } from 'vue';
import { LoginAPI } from '@/http/api';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const loginResult = ref('');
const isLoginFailed = ref(0);
const isUsernameInvalid = ref(false);
const isPasswordInvalid = ref(false);

const router = useRouter();

const handleLogin = () => {
  if (!username.value) {
    isUsernameInvalid.value = true;
    return;
  } else {
    isUsernameInvalid.value = false;
  }
  if (!password.value) {
    isPasswordInvalid.value = true;
    return;
  } else {
    isPasswordInvalid.value = false;
  }

  setTimeout(() => {
    if (username.value === "admin" && password.value === "123456") {
      loginResult.value = "登入成功";
      isLoginFailed.value = 1;
      setTimeout(() => {
        loginResult.value = '';
      }, 1000);
      setTimeout(() => {
        isLoginFailed.value = 0;
      }, 1000);
      const formData = new FormData();
      formData.append("username",username.value);
      formData.append("password",password.value);
      LoginAPI(formData).then(() => {
            router.push({ path: '/' });
        });
    } else {
      loginResult.value = "登入失败";
      isLoginFailed.value = 2;
      ElMessage.error('用户名或密码错误');
      setTimeout(() => {
        loginResult.value = '';
      }, 1000);
      setTimeout(() => {
        isLoginFailed.value = 0;
      }, 1000);
    }
  }, 1000);
};

onMounted(() =>
{
  document.documentElement.style.height = '100%';
  document.body.style.height = '100%';
  document.body.style.flexDirection = 'column';
  document.body.style.backgroundImage = 'linear-gradient(to bottom right, #e0f4ff, #fce0ff)';
});
</script>

<style scoped>


.login-wrapper
{
  width: 100%;
  height: 100vh;
  position: relative;
}

.log_in
{
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 3px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.title
{
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.log_IO .el-input
{
  margin-bottom: 20px;
}

.log_IO .el-button
{
  width: 240px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-bottom: 20px;
}

.status-blue
{
  background-color: #007BFF !important;
}

.status-green
{
  background-color: green !important;
}

.status-red
{
  background-color: red !important;
}

p
{
  font-size: 16px;
  color: #3a3232;
  font-weight: bold;
  margin-top: 10px;
}

:deep(.is-invalid .el-input__inner)
{
  border: 1px solid #dc3545 !important;
}

.invalid-feedback
{
  color: #dc3545;
  font-size: 12px;
  margin-top: 5px;
}
</style>
