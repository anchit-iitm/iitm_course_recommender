<template> 
    <v-navigation-drawer color="primary">
      <v-list-item height="60">
      <v-list-item-title class="text-h5 text-center">Course Compass</v-list-item-title>
      <v-list-item-subtitle class="text-center">Management Panel</v-list-item-subtitle>
    </v-list-item>
    <v-divider></v-divider>

      <v-list nav>
        <v-list-item prepend-icon="mdi-home" title="Dashboard" value="dashboard" :to="{name: 'ManagementDashboard'}"></v-list-item>
        <v-list-item prepend-icon="mdi-home" title="Course List" value="Course List" :to="{name: 'ManagementCourseList'}"></v-list-item>
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

