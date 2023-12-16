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
    component: () => import('@/layouts/admin/Layout.vue'),
    children: [
        {
            name: 'AdminDashboard',
            path: '/admin/dashboard',
            component: () => import('@/views/AdminDashboard.vue'),
        },

        {
          name: 'CTMView',
          path: '/admin/ctm',
          component: () => import('@/views/CourseTeamView.vue'),
      },

    ]
},
{
  path: '/courseTeam',
  redirect: '/courseTeam/dashboard',    
  component: () => import('@/layouts/course_team/Layout.vue'),
  children: [
      {
          name: 'CourseTeamDashboard',
          path: '/courseTeam/dashboard',
          component: () => import('@/views/CourseTeamDashboard.vue'),
      },
  ]
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
