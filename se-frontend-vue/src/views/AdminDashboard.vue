<template>
    <v-container fill-height fluid class="down-top-padding">
      <v-row>        
        <v-col v-for="item in cards" cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title>{{ item.title }}</v-card-title>
            <v-divider />
            <v-card-text>{{ item.text }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>      
    </v-container>
  </template>
  
  
  <script>
  export default {
    data(){
      return {
        cards: [
          {
            title: "Student Details",
            text: "Lorem ipsum"
          },
          {
            title: "Student Details",
            text: "Lorem ipsum"
          },
          {
            title: "Student Details",
            text: "Lorem ipsum"
          }
        ]
      }
    }
  }
  
  </script>