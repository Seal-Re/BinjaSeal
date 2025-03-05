import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login/index.vue'),
        meta: {
            title: '登入',
            layout: false,
        },
    },
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/Home/index.vue'),
      meta: {
        title: '首页',
        layout: true,
      }
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
});

router.beforeEach((to, from, next) => {
  // 白名单路径
  /*const allowList = ['/login', '/404'];*/
  next('/login');
  /*
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    if (!allowList.includes(to.path)) {
      next('/login')
    }
  } else {
    next()
  }*/
})

export default router;
