<template>
  <v-container>    
      <v-form fast-fail @submit.prevent="save">
        <v-row>
          <v-col cols="12" md="6">
        
        <v-card>
          <v-card-title>User Profile</v-card-title>
          <v-card-text>
            <v-select
              :items="[{ 'id': 'foundation', 'name': 'Foundation' }, { 'id': 'diploma', 'name': 'Diploma' }, { 'id': 'degree', 'name': 'Degree' }]"
              v-model="current_degree_level" label="Current Degree Level" item-title="name" item-value="id"></v-select>

            <v-select
              :items="[{ 'id': 'dp', 'name': 'Diploma in Programming' }, { 'id': 'ds', 'name': 'Diploma in Data Science' }, { 'id': 'both', 'name': 'Both' }]"
              v-model="dp_ds" item-title="name" item-value="id" label="Preferred Stream for Recommendations"></v-select>

            <v-select v-model="max_courses" :items="[2, 3, 4]" label="Maximum Courses" type="number" class="mb-5"
              hint="Pick the maximum number of courses you wish to take in upcoming terms" persistent-hint></v-select>

            <v-select :items="all_courses" v-model="current_courses" item-title="name" item-value="id"
              label="Current Courses" multiple hint="Pick the courses in your current term" persistent-hint></v-select>
            
              <v-btn type="submit" block class="mt-5" color="primary">Submit</v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Completed Course Details</v-card-title>
          <v-card-text>

            <v-item-group v-for="(item, k) in completed_courses" :key="k">
              <v-row>
                <v-col cols="12" md="9">
                  <v-autocomplete label="Completed Course" :items="pending_courses" v-model="item.id" item-title="name" class="mb-2"
                    item-value="id" hint="Pick the course you have completed, and its marks"
                    persistent-hint></v-autocomplete>
                </v-col>
                <v-col cols="12" md="2">
                  <v-text-field label="Marks" v-model="item.marks" type="number"></v-text-field>
                </v-col>
                <v-col cols="12" md="1">
                  <v-icon icon="mdi-delete" @click="remove(k)"
                    v-show="k || (!k && completed_courses.length > 1)"></v-icon>
                </v-col>
              </v-row>
              <v-icon icon="mdi-plus" @click="add(k)" v-show="k == completed_courses.length - 1"></v-icon>
            </v-item-group>

            <v-btn type="submit" block class="mt-5" color="primary">Submit</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      </v-row>


      </v-form>

    
  </v-container>
</template>

<script>
export default {
  data: function () {
    return {
      pending_courses: [],
      completed_courses: [],
      current_courses: [],
      all_courses: [],

      current_degree_level: "",
      level_list: "",
      dp_ds: "both",
      max_courses: 2,
    }
  },

  methods: {
    save: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/profile', {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          maximum_courses_in_a_term: this.max_courses,
          current_degree_level: this.current_degree_level,
          dp_or_ds: this.dp_or_ds,
          current_courses: this.current_courses,
          completed_courses: this.completed_courses.map((item) => { item.marks = Number(item.marks); return item })
        })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.message}`)
          }
          this.$root.vtoast.show({ message: "Updated Profile" })
        })
        .catch(error => {
          console.log(error)
          this.$root.vtoast.show({ message: error.message, color: 'error' })
        })
    },

    add() {
      this.completed_courses.push({
        id: '',
        marks: 0
      })
    },

    remove(index) {
      this.completed_courses.splice(index, 1)
    },


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
          this.completed_courses = (data.bio.completed_courses.length > 0) ? data.bio.completed_courses : [{ id: "", marks: 0 }]
          this.current_courses = data.bio.current_courses
          this.current_degree_level = data.bio.current_degree_level
          this.max_courses = data.bio.maximum_courses_in_a_term
          console.log("Profile Data Fetched")
        })
        .catch(error => {
          console.log(error)
        })
    },

    getAllcourses: async function () {
      let token = sessionStorage.getItem("token")
      return fetch('/api/v1/courses/all', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          this.all_courses = data
          this.pending_courses = data

          this.pending_courses = data.filter((course) => {
            const cc = this.completed_courses.map((c) => c.id)
            return !cc.includes(course.id);
          })

        })
        .catch(error => {
          console.log(error)
          // throw Error(error)
        })
    },
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