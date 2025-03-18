import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/store/index';


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path:'/',
        redirect:() =>{
          const isLoggedIn =useUserStore().loginStatus
          return isLoggedIn ? '/home':'/login'
        },
      },
      {
        path:'/login',
        name:'Login',
        component: () => import('@/views/Login/AppIndex.vue'),
        meta: {
          title: '登陆',
          layout: false,
      },
      },
      {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/Home/AppIndex.vue'),
        meta: {
          title: '主页',
          layout: true,
          icon: 'HomeFilled',
      },
      },
      {
        path: '/evaluate',
        name: 'Evaluate',
        component: () => import('@/views/Evaluate/AppIndex.vue'),
        meta: {
          title: '评估',
          layout: true,
      },
      },
      {
        path: '/train',
        name: 'Train',
        component: () => import('@/views/Train/AppIndex.vue'),
        meta: {
          title: '训练',
          layout: true,
      },
      },
    ]
  });

  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const isLoggedIn = userStore.loginStatus;

    if (to.name === 'Login' && isLoggedIn) {
        // 如果已经登录，访问登录页则重定向到主页
        next('/home');
    }
    else {
      // 其他情况正常放行
      next();
    }
});

export default router;
