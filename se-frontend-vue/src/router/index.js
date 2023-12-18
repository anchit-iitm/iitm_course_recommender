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
        component: () => import('@/views/LoginPage.vue'),
      },
      {
        path: '/student/home',
        name: 'StudentHome',
        component: () => import('@/views/student/HomePage.vue'),
      },
      {
        path: '/course/:id',
        name: 'CourseView',
        component: () => import('@/views/student/CoursePage.vue'),
      },
    ],    
  },
  {
    path: '/logout',
    name: 'Logout',    
    beforeEnter: (to, from, next) => {
      sessionStorage.clear()
      next({name: "Login"})
    },  
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    beforeEnter: (to, from, next) => {
      let role = (sessionStorage.getItem("role") == 'admin')
      if (!role){
        console.log("You are not admin")
        next({ name: 'Login' })
      }
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
{
  path: '/courseTeam',
  redirect: '/courseTeam/dashboard',    
  component: () => import('@/layouts/course_team/Layout.vue'),
  beforeEnter: (to, from, next) => {
    let role = (sessionStorage.getItem("role") == 'ctm')
    if (!role){
      console.log("You are not ctm")
      next({ name: 'Login' })
    }
    else
      next()
  },
  children: [
      {
        name: 'CourseTeamDashboard',
        path: '/courseTeam/dashboard',
        component: () => import('@/views/CourseTeamDashboard.vue'),
      },
      {
        path: '/course/:courseId/feedback',
        name: 'CourseFeedback',
        component: () => import('@/views/CourseFeedback.vue'),
      },
  ]
},
{
  path:'/student/profile',
  component:() => import('@/layouts/default/Default.vue'),
  children: [
    {
      name: 'StudentProfile',
      path: '/student/profile',
      component: () => import('@/views/ProfilePage.vue'),
    }
  ]
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

/* router.beforeEach((to, from, next) => {
  const isAuthenticated = (sessionStorage.getItem("token") === null) ? false : true;
  if (!isAuthenticated) {
    if (to.name !== 'Login' && to.name !== 'Register'){ 
      next({ name: 'Login' })
    } else next()
  }
  else next()
}) */

export default router
