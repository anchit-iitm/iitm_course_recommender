<template>
    <v-snackbar
        :color="color"
        :timeout="timer"
        v-model="showSnackbar"
        bottom
        right
        vertical
    >
      <v-icon left>{{icon}}</v-icon> {{message}}
    </v-snackbar>
  </template>
  
  <script>
  export default {
    name: "vtoast",
    data() {
      return{
        showSnackbar: false,
        message: '',
        color: 'success',
        icon: 'mdi-check',
        timer: 3000
      }
    },
    methods:{
      show(data) {
        this.message = data.message || 'missing "message".'
        this.color = data.color || 'success'
        this.timer = data.timer || 3000
        this.icon = this.chooseIcon(data.color)
        this.showSnackbar = true
      },

      chooseIcon(color) {        
        if (color == "success" || color == undefined){
          return 'mdi-check'
        } else if (color == "error"){
          return 'mdi-alert-circle'
        } else if (color == "info") {
          return 'mdi-information'
        } else {
          return 'mdi-alert'
        }
      },
    }
  }
  </script>