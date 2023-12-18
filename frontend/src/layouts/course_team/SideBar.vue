<template>
  <v-navigation-drawer color="primary" v-model="drawer" :rail="rail" permanent @click="rail = false">

    <v-list-item height="60">
      <v-list-item-title class="text-h5 text-center">Course Compass</v-list-item-title>
      <v-list-item-subtitle class="text-center">CTM Panel</v-list-item-subtitle>
    </v-list-item>
    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home" title="My Courses" value="dashboard"
        :to="{ name: 'CourseTeamDashboard' }"></v-list-item>
      <v-list-item prepend-icon="mdi-book-open-blank-variant" title="Feedbacks" value="feedback" @click="showCoursesDropdown"
        append-icon="mdi-chevron-down"></v-list-item>

      <!-- Conditionally render the course list based on showDropdown -->
      <v-list-item prepend-icon="mdi-arrow-right-thin" v-if="showDropdown" v-for="course in courseList" :key="course.id"
        :to="{ name: 'CourseFeedback', params: { courseId: course.id } }">
        <v-list-item-title>{{ course.id }}</v-list-item-title>
        <v-list-item-subtitle>{{ course.name }}</v-list-item-subtitle>
      </v-list-item>
      <!-- <v-list v-if="showDropdown">
        <router-link v-for="course in courseList" :key="course.id" :to="{ name: 'CourseFeedback', params: { courseId: course.code } }">
            <v-list-item>
               <v-list-item-title>{{ course.name }}</v-list-item-title>
            </v-list-item>
        </router-link>
      </v-list> -->
    </v-list>

    <template v-slot:append>
      <v-list-item height="70" prepend-avatar="@/assets/user.png" :title="user"
        :subtitle="email" nav>        
      </v-list-item>
      <div class="pa-2">
        <v-btn block :to="{ name: 'Logout' }">
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>

  <!-- <v-toolbar color="secondary">
    <v-app-bar-nav-icon></v-app-bar-nav-icon>

    <v-toolbar-title>Course Compass</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon :to="{name: 'Logout'}">
      <v-icon>mdi-export</v-icon>
    </v-btn>
  </v-toolbar> -->
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      drawer: true,
      rail: false,
      user: sessionStorage.getItem('name'),
      email: sessionStorage.getItem('email'),
      // courses: [],
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
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }


          this.courseList = data.filter((item) => {
            let instructors = item.instructors.map((ins) => ins.email)
            return instructors.includes(sessionStorage.getItem("email"))
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