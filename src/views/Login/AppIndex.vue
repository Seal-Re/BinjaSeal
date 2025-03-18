<template>
  <div class="login-wrapper">
    <div class="log_in">
      <div class="title">
        <img class="logo_icon" src="@/assets/rzkh.svg" />
        <div class="text">认知障碍康复系统</div>
      </div>
      <!-- 使用 v-if 和 v-else 进行条件渲染 -->
      <div v-if="RegisterFlag === 0" class="log_IO">
        <el-form :model="login" label-width="auto" style="max-width: 600px">
          <el-form-item>
            <div class="el_input_wrapper">
              <el-input
                v-model="login.username"
                placeholder="请输入您的用户名"
                clearable
                size="large"
              />
            </div>
          </el-form-item>
          <el-form-item>
            <div class="el_input_wrapper">
              <el-input
                v-model="login.password"
                type="password"
                placeholder="请输入您的密码"
                show-password
                size="large"
              />
            </div>
          </el-form-item>
        </el-form>
        <div class="el_button_wrapper">
          <el-button class="login_button" type="danger" @click="handleLogin">登录</el-button>
        </div>

        <div class="button-group">
          <el-button @click="handleRegister" type="" link> 注册&nbsp;|</el-button>

          <el-button type="" link>忘记密码 </el-button>
        </div>
      </div>
      <div v-else class="log_IO">
        <el-form :model="login" label-width="auto" style="max-width: 600px">
          <el-form-item>
            <div class="el_input_wrapper">
              <el-input
                v-model="login.username"
                placeholder="请输入您的用户名"
                clearable
                size="large"
              />
            </div>
          </el-form-item>
          <el-form-item>
            <div class="el_input_wrapper">
              <el-input
                v-model="login.password"
                type="password"
                placeholder="请输入您的密码"
                show-password
                size="large"
              />
            </div>
          </el-form-item>
        </el-form>
        <div class="el_button_wrapper">
          <el-button class="login_button" type="danger" @click="handleRegister_ex">注册</el-button>
        </div>

        <div class="button-group">
          <el-button @click="handleLogin_ex" type="" link> 登录&nbsp;|</el-button>

          <el-button type="" link>忘记密码 </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import router from "@/router/index";
import axios from "axios";
import { useUserStore } from "@/store/index";
import { reactive } from "vue";
import { ElMessage } from 'element-plus';
import baseurl from '@/http/base';

const login = reactive({
  username: "",
  password: "",
});

const userStore = useUserStore();
const isLoginFailed = ref(0);
const isRegisterFailed = ref(0);
const RegisterFlag = ref(0);

const handleRegister = async () => {
  RegisterFlag.value = 1;
};
const handleLogin_ex = async () => {
  RegisterFlag.value = 0;
};

const handleRegister_ex = async () => {
  const userData = {
    username: login.username,
    password: login.password,
  };

  try {
    const response = await axios.post(baseurl+'/register', userData);
    if (response.data.success) {
      isRegisterFailed.value = 1;
      setTimeout(() => {
        isRegisterFailed.value = 0;
      }, 1000);
      ElMessage.success('注册成功，请登录');
      RegisterFlag.value = 0;
    } else {
      isRegisterFailed.value = 2;
      setTimeout(() => {
        isRegisterFailed.value = 0;
      }, 1000);
    }
  } catch (error) {
    console.error('注册请求出错:', error);
    isRegisterFailed.value = 2;
    setTimeout(() => {
      isRegisterFailed.value = 0;
    }, 1000);
  }
};
const handleLogin = async () => {
  const userData = {
    username: login.username,
    password: login.password,
  };

  try {
    const response = await axios.post(baseurl+"/login", userData);
    if (response.data.success) {
      isLoginFailed.value = 1;
      setTimeout(() => {
        isLoginFailed.value = 0;
      }, 1000);

      // 假设服务器返回的响应中包含 token 和 userInfo
      const { token, userInfo } = response.data;

      // 使用 userStore 的方法设置 token 和 userInfo
      userStore.setToken(token);
      userStore.setUserInfo(userInfo);

      router.push("/home");
    } else {
      isLoginFailed.value = 2;
      setTimeout(() => {
        isLoginFailed.value = 0;
      }, 1000);
    }
  } catch (error) {
    console.error("登录请求出错:", error);
    isLoginFailed.value = 2;
    setTimeout(() => {
      isLoginFailed.value = 0;
    }, 1000);
  }
};

onMounted(() => {
  document.documentElement.style.height = "100%";
  document.body.style.height = "100%";
  document.body.style.flexDirection = "column";
  document.body.style.backgroundColor = "#FFFFFFF";
});
</script>

<style scoped>
.login-wrapper {
  width: 100%;
  height: 100vh;
  position: relative;
}

.log_in {
  width: 400px;
  height: 400px;
  padding: 32px 44px;
  border: 1px solid #ccc;
  border-radius: 3px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #ffffff;
}

.title {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 45px;
 .logo_icon {
    width: 60px;
    height: 60px;
    padding-right: 20px;
  }
 .text {
    font-size: 24px;
    color: #333;
    padding: 20px 0;
  }
}

.el_input_wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px; /* 根据实际需求调整高度 */
  width: 100%; /* 根据实际需求调整宽度 */
  border-radius: 4px;
}
.el-input {
  width: 100%;
  height: 100%;
}
.el_button_wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px; /* 根据实际需求调整高度 */
  width: 100%; /* 根据实际需求调整宽度 */
  border-radius: 4px;
}
.login_button {
  width: 100%;
  height: 100%;
  font-size: 20px;
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-group .el-button {
  color: gray;
  border: none;
  padding-top: 30px;
  margin-left: 0;
}

.status-blue {
  background-color: #007bff !important;
}

.status-green {
  background-color: green !important;
}

.status-red {
  background-color: red !important;
}

p {
  font-size: 16px;
  color: #3a3232;
  font-weight: bold;
  margin-top: 10px;
}
</style>
