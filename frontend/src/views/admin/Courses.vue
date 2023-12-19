<template>
  <v-container>
    <v-card elevation="2">
      <v-data-table :headers="headers" :items="courses" :group-by="groupBy" items-per-page=25>
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Courses</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>

            <v-dialog v-model="addDialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="primary" dark class="mb-2" v-bind="props">
                  Add Course
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">Add Course</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-text-field v-model="addCourse.id" label="Course Code"></v-text-field>
                    </v-row>
                    <v-row>
                      <v-text-field v-model="addCourse.name" label="Course Name"></v-text-field>
                    </v-row>
                    <v-row>
                      <v-select :items="['foundation', 'diploma', 'degree']" v-model="addCourse.level" label="Course Level"></v-select>
                    </v-row>
                    <v-row>
                      <v-autocomplete v-model="addCourse.instructors" label="Course Team Members" :items="all_emails"
                        item-title="email" multiple return-object></v-autocomplete>
                    </v-row>

                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="secondary" variant="text" @click="closeAdd">
                    Cancel
                  </v-btn>
                  <v-btn color="primary" variant="text" @click="saveAdd">
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-dialog v-model="dialog" max-width="500px">              
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-text-field v-model="editedItem.name" label="Course Name"></v-text-field>
                    </v-row>
                    <v-row>
                      <v-autocomplete v-model="editedItem.instructors" label="Course Team Members" :items="all_emails"
                        item-title="email" multiple return-object></v-autocomplete>
                    </v-row>

                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="secondary" variant="text" @click="close">
                    Cancel
                  </v-btn>
                  <v-btn color="primary" variant="text" @click="save">
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="text-center">Are you sure you want to delete this item?</v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="closeDelete">Cancel</v-btn>
                  <v-btn color="red" @click="deleteItemConfirm">OK</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.instructors="{ item }">
          <p class="mt-2" v-for="x in item.instructors">{{ x.name }}</p>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon size="small" class="me-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon size="small" @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize">
            Reset
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    groupBy: [
      {
        key: 'level',
      },
    ],
    all_emails: [],
    search: '',
    courses: [],
    dialog: false,
    addDialog: false,
    addCourse: {
      id: "",
      name: "",
      instructors: [],
      level: ""
    },
    dialogDelete: false,
    headers: [
      {
        title: 'Course Code',
        align: 'start',
        key: 'id',
      },
      { title: 'Name', key: 'name' },
      { title: 'Difficulty Rating', key: 'difficulty_rating' },
      { title: 'Instructors', key: 'instructors' },
      { title: 'Actions', key: 'actions', sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      name: '',
      instructors: []
    },
    defaultItem: {
      name: '',
      instructors: []
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Add Course' : 'Edit Course'
    },

    editMode() {
      return this.editedIndex === -1 ? false : true
    },
  },

  watch: {
    dialog(val) {
      val || this.close()
    },
    addDialog(val) {
      val || this.closeAdd()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
  },

  created() {
    this.initialize()
  },

  methods: {
    initialize: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/courses/all', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },

      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          this.courses = data

        })
        .catch(error => {
          console.log(error)
        })

      await fetch('/api/v1/admin', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },

      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          for (var item in data) {
            if (data[item].role == "ctm") {
              this.all_emails.push({
                email: data[item].email,
                name: data[item].name,
                role: data[item].role,
                created_at: data[item].created_at
              })
            }
          }
        })
        .catch(error => {
          // toastr.error(error.message, 'Error')
          console.log(error)
        })
    },

    editItem(item) {
      this.editedIndex = this.courses.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item) {
      this.editedIndex = this.courses.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm: async function () {      
      this.closeDelete()
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/courses/' + this.courses[this.editedIndex].id, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))        
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.message}`)
          }          
          this.courses.splice(this.editedIndex, 1)
          this.$root.vtoast.show({ message: "Course Deleted", color: "warning" })
        })
        .catch(error => {
          this.$root.vtoast.show({ message: error.message, color: "error" })
        })      
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeAdd() {
      this.addDialog = false
      this.$nextTick(() => {
        this.addCourse = Object.assign({}, {
      id: "",
      name: "",
      instructors: [],
      level: ""
    })        
      })
    },

    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/courses/' + this.editedItem.id, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "name": this.editedItem.name,
          "instructors": this.editedItem.instructors,
        })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          Object.assign(this.courses[this.editedIndex], this.editedItem)
          this.$root.vtoast.show({ message: "Course Info Updated" })
        })
        .catch(error => {
          this.$root.vtoast.show({ message: error.message, color: "error" })
        })
      this.close()
    },

    saveAdd: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/courses/all', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "code": this.addCourse.id,
          "name": this.addCourse.name,
          "instructors": this.addCourse.instructors,
          "level": this.addCourse.level
        })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          this.courses.push(this.addCourse)          
          this.$root.vtoast.show({ message: "Course Added" })
        })
        .catch(error => {
          this.$root.vtoast.show({ message: error.message, color: "error" })
        })
      this.closeAdd()
    },
  },
}
</script>