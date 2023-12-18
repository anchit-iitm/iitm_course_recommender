<template>
  <v-navigation-drawer color="primary">
    <v-list>
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
        :title="user"
        :subtitle="email"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list nav>
      <v-list-item
        prepend-icon="mdi-home"
        title="Dashboard"
        value="dashboard"
        :to="{ name: 'CourseTeamDashboard' }"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-book-open-blank-variant"
        title="Courses"
        value="courses"
        @click="showCoursesDropdown"
      ></v-list-item>

      <!-- Conditionally render the course list based on showDropdown -->
      <v-list-item v-if="showDropdown" v-for="course in courses" :key="course.id" :to="{ name: 'CourseFeedback', params: { courseId: course.id } }">
        <v-list-item-title>{{ course.name }}</v-list-item-title>
      </v-list-item>
      <!-- <v-list v-if="showDropdown">
        <router-link v-for="course in courseList" :key="course.id" :to="{ name: 'CourseFeedback', params: { courseId: course.code } }">
            <v-list-item>
               <v-list-item-title>{{ course.name }}</v-list-item-title>
            </v-list-item>
        </router-link>
      </v-list> -->
    </v-list>
  </v-navigation-drawer>

  <v-toolbar color="secondary">
    <v-app-bar-nav-icon></v-app-bar-nav-icon>

    <v-toolbar-title>Course Compass</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon :to="{name: 'Logout'}">
      <v-icon>mdi-export</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      user: sessionStorage.getItem('name'),
      email: sessionStorage.getItem('email'),
courses: [],
      courseList: [{
          id: 'CS101',
          name: 'Introduction to Computer Science',
          description: 'An introductory course covering fundamental concepts in computer science.',
          difficulty_rating: 4.5,
          level: 'foundation',
          dp_or_ds: 'both',
          credits: 3,
        },
        {
          id: 'MATH201',
          name: 'Calculus II',
          description: 'A continuation of Calculus I, focusing on advanced calculus topics.',
          difficulty_rating: 5.0,
          level: 'degree',
          dp_or_ds: 'both',
          credits: 4,
        }], // Stores course data
    };
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize: async function () {
      let token = sessionStorage.getItem("token")
            await fetch('/api/v1/courses/all', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
                },
                
            })
            .then(response => response.json().then(jdata=> ({response: response, data: jdata})))
            .then(({response, data}) => {
                if(!response.ok){
                    throw new Error(`Error ${response.status}: ${data.msg}`)
                }
                this.courses = data
                console.log('Fetched Data:', this.cards);
                
                let courses_list = data.filter((item) => {                    
                    let instructors = item.instructors.filter((ins) => ins.email)
                    return instructors.includes(sessionStorage.getItem("token"))
                  })
                
            })
            .catch(error => {
          console.log(error)
            })
    },

    showCoursesDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>