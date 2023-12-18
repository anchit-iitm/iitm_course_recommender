<template>
    <v-app>
      <v-main>
  
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Foundation Courses ({{ foundation.length }})</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list>
                    <v-list-item v-for="(item, index) in foundation" append-icon="mdi-information" :to="{name: 'CourseView', params: {id: item.id}}">
                      <v-list-item-title>{{ item.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ item.id }} | Marks: {{ item.marks }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Diploma Courses ({{ diploma.length }})</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list>
                    <v-list-item v-for="(item, index) in diploma" append-icon="mdi-information" :to="{name: 'CourseView', params: {id: item.id}}">
                      <v-list-item-title>{{ item.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ item.id }} | Marks: {{ item.marks }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col> 
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Degree Courses ({{ degree.length }})</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list>
                    <v-list-item v-for="(item, index) in degree" append-icon="mdi-information" :to="{name: 'CourseView', params: {id: item.id}}">
                      <v-list-item-title>{{ item.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ item.id }} | Marks: {{ item.marks }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col> 
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>


<script>
export default {
  data: function () {
    return {
      foundation: [],
      diploma: [],
      degree: [],
    }
  },

  methods: {
    getCourseInfo: async function (courseCode) {
      let token = sessionStorage.getItem("token")      
      return fetch('/api/v1/courses/' + courseCode, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          console.log(courseCode + " fetched")
          return data
        })
        .catch(error => {
          console.log(error)
          throw Error(error)
        })
    },

    getCompletedCourses: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {                    
          data.bio.completed_courses.forEach((course) => this.getCourseInfo(course.id).then(r => {
            r.marks = course.marks            
            if(r.level == 'foundation'){
                this.foundation.push(r)
            } else if(r.level == 'diploma'){
                this.diploma.push(r)
            } else {
                this.degree.push(r)
            }
            
        }))          
          console.log("Current Courses Fetched")
        })
        .catch(error => {
          console.log(error)
        })
    },
  },

  mounted: async function () {
    this.getCompletedCourses()
  }

}
</script>