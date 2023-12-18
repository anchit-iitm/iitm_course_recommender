<template>
  <v-container>
    <v-card elevation="2">
      <v-data-table :headers="headers" :items="admins" :group-by="groupBy" items-per-page=25>
        <template v-slot:group-header="{ item, columns, toggleGroup, isGroupOpen }">
          <tr>
            <td :colspan="columns.length">
              <VBtn size="small" variant="text" :icon="isGroupOpen(item) ? '$expand' : '$next'"
                @click="toggleGroup(item)"></VBtn>
              {{ item.value == "admin" ? 'Administrators' : (item.value == 'ctm' ? 'Course Team Members' : "IITM Management")
              }}
            </td>
          </tr>
        </template>

        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Admin Members</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="primary" dark class="mb-2" v-bind="props">
                  Add Administrator
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-text-field v-if="editMode" v-model="editedItem.id" label="Email Address" readonly></v-text-field>

                      <v-autocomplete v-else v-model="editedItem.id" label="Email Address" :items="all_emails"
                        item-title="id" return-object></v-autocomplete>
                    </v-row>
                    <v-row>
                      <v-autocomplete v-model="editedItem.role" label="Access Level"
                        :items="['admin', 'ctm', 'im']"></v-autocomplete>
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
        key: 'role',
        order: 'asc',
      },
    ],
    all_emails: [],
    search: '',
    admins: [],
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        title: 'Email',
        align: 'start',
        key: 'id',
      },
      { title: 'Name', key: 'name' },
      { title: 'Created At', key: 'created_at' },
      { title: 'Actions', key: 'actions', sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      id: '',
      role: ''
    },
    defaultItem: {
      id: '',
      role: 'admin'
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Add Member' : 'Edit Member'
    },

    editMode() {
      return this.editedIndex === -1 ? false : true
    },
  },

  watch: {
    dialog(val) {
      val || this.close()
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
            this.admins.push({
              id: data[item].email,
              name: data[item].name,
              role: data[item].role,
              created_at: data[item].created_at
            })
          }
        })
        .catch(error => {
          console.log(error)
        })

      await fetch('/api/v1/student/all', {
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
            this.all_emails.push({
              id: data[item].email,
              name: data[item].name,
              role: data[item].role,
              created_at: data[item].created_at
            })
          }
        })
        .catch(error => {
          // toastr.error(error.message, 'Error')
          console.log(error)
        })
    },

    editItem(item) {
      this.editedIndex = this.admins.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item) {
      this.editedIndex = this.admins.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm: async function () {
      this.closeDelete()
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/admin', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "email": this.admins[this.editedIndex].id,
        })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          this.admins.splice(this.editedIndex, 1)
        })
        .catch(error => {
          if (error.message.includes("Token has expired")) {
            // toastr.error("Re-login required, token has expired", 'Error')
            // this.$router.push("/relogin")
          }
          // toastr.error(error.message, 'Error')
          console.log(error)
        })
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
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
      await fetch('/api/v1/admin', {
        method: this.editedIndex > -1 ? 'PATCH' : 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "email": this.editedIndex > -1 ? this.editedItem.id : this.editedItem.id.id,
          "role": this.editedItem.role,
        })
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          if (!response.ok) {
            if (data.error != null) {
              this.errors.push(data.error)
              throw new Error(`Error ${response.status}: ${data.error}`)
            } else {
              this.errors.push(data.msg)
              throw new Error(`Error ${response.status}: ${data.msg}`)
            }
          }
          if (this.editedIndex > -1) {
            Object.assign(this.admins[this.editedIndex], this.editedItem)
          } else {
            this.all_emails.splice(this.all_emails.findIndex(a => a.id === this.editedItem.id.id), 1)
            this.editedItem.id.role = this.editedItem.role
            this.admins.push(this.editedItem.id)
          }
        })
        .catch(error => {
          console.log(error)
        })


      this.close()
    },
  },
}
</script>