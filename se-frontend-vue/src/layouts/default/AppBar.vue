<template>
  <div>
    <v-toolbar color="primary">
      <!-- <v-img
        class="mx-2"
        src="@/assets/logo2.png"
        max-height="60"
        max-width="60"
        contain
      ></v-img> -->
      <v-toolbar-title>Course Compass</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon :to="{name: 'Logout'}">
        <v-icon>mdi-export</v-icon>
      </v-btn>
    </v-toolbar>
  </div>
</template>
