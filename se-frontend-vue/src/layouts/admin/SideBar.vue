<template>
  <v-navigation-drawer color="primary" v-model="drawer" :rail="rail" permanent @click="rail = false">

    <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" :title="user" :subtitle="email" nav>
      <template v-slot:append>
        <v-btn variant="text" icon="mdi-chevron-left" @click.stop="rail = !rail"></v-btn>
      </template>
    </v-list-item>


    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home" title="Dashboard" value="dashboard"
        :to="{ name: 'AdminDashboard' }"></v-list-item>
      <v-list-item prepend-icon="mdi-book-open-blank-variant" title="Courses" value="courses"
        :to="{ name: 'AdminsCourseList' }"></v-list-item>
      <v-list-item prepend-icon="mdi-account-outline" title="All Administrators" value="admins"
        :to="{ name: 'AdminsList' }"></v-list-item>
    </v-list>
    <template v-slot:append>
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

      <v-btn :to="{name: 'Logout'}" icon>
        <v-icon>mdi-export</v-icon>
      </v-btn>
    </v-toolbar> -->
</template>

<script>
export default {
  data: function () {
    return {
      user: sessionStorage.getItem("name"),
      email: sessionStorage.getItem("email"),
      drawer: true,
      rail: false,
    }
  },
}
</script>
