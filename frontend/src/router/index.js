// Composables
import { createRouter, createWebHashHistory } from 'vue-router'


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
    children: [
      {
        path: '/register',
        name: 'Register',
        meta:{sidebar:false},
        component: () => import('@/views/RegisterPage.vue'),
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
            } else if(role == "im"){
              return {name:"ManagementDashboard"}
            }
          }
        },
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
            } else if(role == "im"){
              return {name:"ManagementDashboard"}
            }
          }
        },
      },
      {
        path: '/logout',
        name: 'Logout',    
        beforeEnter: (to, from) => {
          sessionStorage.clear()      
          return {name: "Login"}
        },  
      },
    ],    
  },
  {
    path: '/student',
    component: () => import('@/layouts/student/Default.vue'),
    beforeEnter: (to, from) => {
      let role = (sessionStorage.getItem("role") == 'student')
      if (!role){
        console.log("You are not student")
        return { name: 'Login' }
      }
    },
    children: [      
      {
        path: '/student/home',
        name: 'StudentHome',
        component: () => import('@/views/student/Home.vue'),
        beforeEnter: [requireLogin],
      },
      {
        path: '/courses/:id',
        name: 'CourseView',
        component: () => import('@/views/student/SingleCourse.vue'),
        beforeEnter: [requireLogin],
      },
      {
        path: '/courses/completed',
        name: 'CompletedCourses',
        component: () => import('@/views/student/CompletedCourses.vue'),
        beforeEnter: [requireLogin],
      },
      {
        path: '/courses/all',
        name: 'AllCourses',
        component: () => import('@/views/student/AllCourses.vue'),
        beforeEnter: [requireLogin],
      },
      {
        name: 'StudentProfile',
        path: '/student/profile',
        component: () => import('@/views/student/Profile.vue'),
        beforeEnter: [requireLogin],
      }
    ],    
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
            component: () => import('@/views/admin/Dashboard.vue'),
            beforeEnter: [requireLogin],
        },

        {
          name: 'AdminsList',
          path: '/admin/all',
          component: () => import('@/views/admin/ListOfAdmins.vue'),
          beforeEnter: [requireLogin],
        },

        {
          name: 'AdminsCourseList',
          path: '/admin/courses/all',
          component: () => import('@/views/admin/Courses.vue'),
          beforeEnter: [requireLogin],
        },

    ]
},
{
  path: '/ctm',
  redirect: '/ctm/dashboard',    
  component: () => import('@/layouts/course_team/Layout.vue'),
  beforeEnter: (to, from) => {
    let role = (sessionStorage.getItem("role") == 'ctm')
    if (!role){
      console.log("You are not ctm")
      return { name: 'Login' }
    }
  },
  children: [
      {
        name: 'CourseTeamDashboard',
        path: '/ctm/dashboard',
        component: () => import('@/views/ctm/Dashboard.vue'),
        beforeEnter: [requireLogin],
      },
      {
        name: 'CourseFeedback',
        path:'/ctm/course/:courseId/feedback',
        component: () => import('@/views/ctm/Feedback.vue'),
        beforeEnter: [requireLogin],
      }
  ]
},

{
  path:'/im',
  redirect: '/im/dashboard',
  beforeEnter: (to, from) => {
    let role = (sessionStorage.getItem("role") == 'im')
    if (!role){
      console.log("You are not im")
      return { name: 'Login' }
    }
  },
  component:() => import('@/layouts/management/Layout.vue'),
  children: [
    {
      name: 'ManagementDashboard',
      path: '/im/dashboard',
      component: () => import('@/views/management/Dashboard'),
      beforeEnter: [requireLogin],
    },
    {
      name: 'ManagementCourseList',
      path: '/im/courses/all',
      component: () => import('@/views/management/CourseList'),
      beforeEnter: [requireLogin],
    },
    {
      name: 'IMCourseFeedback',
      path:'/im/course/:courseId/feedback',
      component: () => import('@/views/ctm/Feedback.vue'),
      beforeEnter: [requireLogin],
    }
  ]
},

]

const router = (app) => createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes: routes(app),  
})
export default router
