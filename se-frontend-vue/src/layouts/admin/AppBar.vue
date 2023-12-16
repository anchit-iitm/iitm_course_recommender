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
          <v-list-item prepend-icon="mdi-home" title="Dashboard" value="dashboard" :to="{name: 'AdminDashboard'}"></v-list-item>
          <v-list-item prepend-icon="mdi-book-open-blank-variant" title="Courses" value="courses" :to="{name: 'AdminsCourseList'}"></v-list-item>
          <v-list-item prepend-icon="mdi-account-outline" title="All Administrators" value="admins" :to="{name: 'AdminsList'}"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-toolbar color="secondary">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>Course Compass</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn :to="{name: 'Logout'}" icon>
        <v-icon>mdi-export</v-icon>
      </v-btn>
    </v-toolbar>
</template>

<script>
export default {
  data: function(){
          return {              
              user: sessionStorage.getItem("name"),
              email: sessionStorage.getItem("email")
          }
      },
  }
</script>
