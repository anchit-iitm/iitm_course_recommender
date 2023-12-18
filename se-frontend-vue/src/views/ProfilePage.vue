<template>
    <v-app>
        <v-main>
            <v-container>
                <p class="text-h5 text-center">My Profile</p>
            </v-container>
            <v-container>
                <v-card>
                    <v-card-title>Current Degree Level</v-card-title>
                    <v-select
                    :items="level_list"
                    v-model="current_degree_level"
                    return-object
                    @change="ChangeLevel"
                    ></v-select>
                </v-card>
            </v-container>
            <v-container>
                <v-card>
                    <v-card-title>Completed Courses</v-card-title>
                    <v-list lines="one">
                    <v-list-item
                        v-for="(item, index) in completed_courses"
                        :title="item.id"
                        :subtitle="'Score: ' + item.marks"
                    ></v-list-item>
                    </v-list>
                    <v-select
                     :items="all_courses"
                     item-text ="id"
                    ></v-select>
                </v-card>
            </v-container>
            <v-container>
                <v-card>
                    <v-card-title>Current Courses</v-card-title>
                    <v-list lines="one">
                    <v-list-item
                        v-for="(item, index) in current_courses"
                        :title="item.id +': '+item.name"
                    ></v-list-item>
                    </v-list>
                    <v-select
                     :items="all_courses"
                     item-text ="id"
                    ></v-select>
                </v-card>
            </v-container>
            <v-container>
                <v-card>
                    <v-card-title>Maximum Courses Permitted</v-card-title>
                    <v-card-text>{{ max_courses }}</v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import cydagre from "cytoscape-dagre";
import cytoscape from "cytoscape";
export default {
  data: function () {
    return {
      completed_courses: [],
      current_courses: [],
      all_courses: [],
      current_degree_level: "",
      level_list: ["foundation", "diploma", "degree"],
      dp: false,
      max_courses: 2,
    }
  },

  methods: {
    getCourseInfo: async function (courseCode) {
      let token = sessionStorage.getItem("token")
      let data = ""
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

    getProfile: async function () {
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
          sessionStorage.setItem("pic", data.pic)
          this.completed_courses = data.bio.completed_courses
          data.bio.current_courses.forEach((courseCode) => this.getCourseInfo(courseCode).then(r => this.current_courses.push(r)))
          this.current_degree_level = data.bio.current_degree_level
          this.max_courses = data.bio.maximum_courses_in_a_term
          console.log("Profile Data Fetched")
        })
        .catch(error => {
          console.log(error)
        })
    },

    ChangeLevel: async function () {
        console.log(this.current_degree_level)
        let token = sessionStorage.getItem("token")
        await fetch('/api/v1/profile', {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
                    "current_degree_level": this.current_degree_level
                })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({response, data}) => {
                if(!response.ok){
                    if(data.error != null){
                        this.errors.push(data.error)
                        throw new Error(`Error ${response.status}: ${data.error}`)
                    } else {
                        this.errors.push(data.msg)
                        throw new Error(`Error ${response.status}: ${data.msg}`)
                    }
                }                
                else{
                    this.getProfile()
                }
            })
            .catch(error => {
                console.log(error)
            })
    },
    getAllcourses: async function () {
      let token = sessionStorage.getItem("token")
      let data = ""
      return fetch('/api/v1/courses/all' , {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          console.log("all courses fetched")
          this.all_courses=Object.values(data)
          console.log(this.all_courses)
        })
        .catch(error => {
          console.log(error)
          throw Error(error)
        })
    }

    },
    mounted: async function () {
    this.getProfile()
    this.getAllcourses()
  }
}
</script>

<style lang="scss">
// #container {
//   height: 600px;
//   width: 960px;
// }
#cy {
  height: 1500px;
  width: 960px;
}
</style>