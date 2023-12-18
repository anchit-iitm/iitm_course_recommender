// Composables
import { createRouter, createWebHistory } from 'vue-router'


const requireLogin = (to, from) => {
  const isAuthenticated = (sessionStorage.getItem("token") === null) ? false : true;
  if (!isAuthenticated) {
    if (to.name !== 'Login' && to.name !== 'Register'){ 
      return { name: 'Login' }
    }
  }
}


const routes = (app) => [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '/register',
        name: 'Register',
        meta:{sidebar:false},
        component: () => import('@/views/RegisterPage.vue'),
      },
      {
        path: '',
        name: 'Login',
        meta:{sidebar:false},
        component: () => import('@/views/LoginPage.vue'),
        beforeEnter: (to, from) => {
          const isAuthenticated = (sessionStorage.getItem("token") === null) ? false : true;
          if (isAuthenticated){
            let role = sessionStorage.getItem("role")
            if(role == "admin"){
              return {name:"AdminDashboard"}
            } else if(role == "student"){
              return {name:"StudentHome"}
            } else if(role == "ctm"){
              return {name:"CourseTeamDashboard"}
            }
          }
        },
      },
      {
        path: '/student/home',
        name: 'StudentHome',
        component: () => import('@/views/student/HomePage.vue'),
        beforeEnter: [requireLogin],
      },
      {
        path: '/courses/:id',
        name: 'CourseView',
        component: () => import('@/views/student/CoursePage.vue'),
        beforeEnter: [requireLogin],
      },
      {
        path: '/courses/completed',
        name: 'CompletedCourses',
        component: () => import('@/views/student/CompletedCourses.vue'),
        beforeEnter: [requireLogin],
      },
      {
        name: 'StudentProfile',
        path: '/student/profile',
        component: () => import('@/views/ProfilePage.vue'),
        beforeEnter: [requireLogin],
      }
    ],    
  },
  {
    path: '/logout',
    name: 'Logout',    
    beforeEnter: (to, from) => {
      sessionStorage.clear()      
      return {name: "Login"}
    },  
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    beforeEnter: (to, from) => {
      let role = (sessionStorage.getItem("role") == 'admin')
      if (!role){
        console.log("You are not admin")
        return { name: 'Login' }
      }
    },
    component: () => import('@/layouts/admin/Layout.vue'),
    children: [
        {
            name: 'AdminDashboard',
            path: '/admin/dashboard',
            component: () => import('@/views/AdminDashboard.vue'),
            beforeEnter: [requireLogin],
        },

        {
          name: 'AdminsList',
          path: '/admin/all',
          component: () => import('@/views/AdminAllView.vue'),
          beforeEnter: [requireLogin],
        },

        {
          name: 'AdminsCourseList',
          path: '/admin/courses/all',
          component: () => import('@/views/AdminCourses.vue'),
          beforeEnter: [requireLogin],
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
},

{
  path:'/management',
  redirect: '/management/dashboard',
  
  component:() => import('@/layouts/management/Layout.vue'),
  children: [
    {
      name: 'ManagementDashboard',
      path: '/management/dashboard',
      component: () => import('@/views/management/ManagementDashboard'),
    },
    {
      name: 'ManagementCourseList',
      path: '/management/courseList',
      component: () => import('@/views/management/CourseList'),
    }
  ]
},
{
  name: 'CourseFeedback',
  path:'/feedback/:courseId',
  component: () => import('@/views/Feedback.vue')
}

]

const router = (app) => createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes(app),  
})
export default router
