// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Login',
        // route level code-splitting
        // this generates a separate chunk (Home-[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import('@/views/LoginPage.vue'),
      },      
    ],    
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    beforeEnter: (to, from, next) => {
      let role = (sessionStorage.getItem("role") === 'admin')
      if (!role)
        next({ name: 'Login' })
      else
        next()
    },    
    component: () => import('@/layouts/admin/Layout.vue'),
    children: [
        {
            name: 'AdminDashboard',
            path: '/admin/dashboard',
            component: () => import('@/views/AdminDashboard.vue'),
        },

        {
          name: 'AdminsList',
          path: '/admin/all',
          component: () => import('@/views/AdminAllView.vue'),
        },

        {
          name: 'AdminsCourseList',
          path: '/admin/courses/all',
          component: () => import('@/views/AdminCourses.vue'),
        },

    ]
},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = (sessionStorage.getItem("token") === null) ? false : true;
  if (!isAuthenticated) {
    if (to.name !== 'Login' && to.name !== 'Register'){ 
      next({ name: 'Login' })
    } else next()
  }
  else next()
})

export default router
