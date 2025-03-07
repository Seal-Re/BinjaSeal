import { defineStore } from 'pinia';

// 定义用户状态存储
export const useUserStore = defineStore('user', {
    // 状态定义
    state: () => ({
        // 存储用户登录状态，初始值为 false 表示未登录
        loginStatus: false,
        // 存储用户信息，初始为空对象
        userInfo: {}
    }),

    // 获取器，类似于计算属性
    getters: {
        // 获取用户是否已登录的状态
        isLoggedIn: (state) => state.loginStatus,
        // 获取用户信息
        getUserInfo: (state) => state.userInfo
    },

    // 操作方法，用于修改状态
    actions: {
        // 用户登录操作，接收用户信息作为参数
        login(userData) {
            this.loginStatus = true;
            this.userInfo = userData;
        },
        // 用户注销操作
        logout() {
            this.loginStatus = false;
            this.userInfo = {};
        }
    }
});
