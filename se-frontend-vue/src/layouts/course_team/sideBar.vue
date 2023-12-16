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
      <v-list v-if="showDropdown">
        <v-list-item v-for="course in courseList" :key="course" @click="handleCourseClick(course.id)">
          <v-list-item-title>{{ course.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-list>
  </v-navigation-drawer>

  <v-toolbar color="secondary">
    <v-app-bar-nav-icon></v-app-bar-nav-icon>

    <v-toolbar-title>Course Compass</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon>
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
      courseList: [{
          code: 'CS101',
          name: 'Introduction to Computer Science',
          description: 'An introductory course covering fundamental concepts in computer science.',
          difficulty_rating: 4.5,
          level: 'foundation',
          dp_or_ds: 'both',
          credits: 3,
        },
        {
          code: 'MATH201',
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
      try {
        let token = sessionStorage.getItem('token');
        const response = await fetch('/api/v1/courses/all', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        // Filter the courses based on the user's token
        this.courseList = data.filter((course) => {
          const instructors = course.instructors.map((ins) => ins.email);
          return instructors.includes(sessionStorage.getItem('email'));
        });
      } catch (error) {
          console.log(error);
      }
    },

    showCoursesDropdown() {
      this.showDropdown = !this.showDropdown;
    },

    handleCourseClick(courseId) {
      // Handle course click as needed
      console.log(`Clicked on course ${courseId}`);
      // You can add additional logic here
    },
  },
};
</script>