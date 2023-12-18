<template>
  <v-navigation-drawer v-if="shouldShowSidebar" color="primary" v-model="drawer" :rail="rail" permanent
    @click="rail = false">

    <v-list-item height="60">
      <v-list-item-title class="text-h5 text-center">Course Compass</v-list-item-title>
    </v-list-item>

    <v-divider></v-divider>




    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home" title="Dashboard" value="dashboard"
        :to="{ name: 'StudentHome' }"></v-list-item>
        <v-list-item prepend-icon="mdi-human" title="My Profile" value="profile"
        ></v-list-item>
      <v-list-item prepend-icon="mdi-book-open-blank-variant" title="Completed Courses" value="courses"
        :to="{ name: 'CompletedCourses' }"></v-list-item>
        
    </v-list>

    <template v-slot:append>
      <v-list-item height="70" prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" :title="user"
        :subtitle="email" nav>
      </v-list-item>
      <div class="pa-2">
        <v-btn block :to="{ name: 'Logout' }">
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      drawer: true,
      rail: false,
      user: "",
      email: "",
    };
  },

  created() {
    this.initialize();
  },

  computed: {
    shouldShowSidebar() {
      return this.$route.meta.sidebar !== false;
    }
  },

  methods: {
    initialize: async function () {
      this.user = sessionStorage.getItem('name')
      this.email = sessionStorage.getItem('email')
    },

    showCoursesDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>
