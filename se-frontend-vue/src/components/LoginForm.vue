<template>
<div class="d-flex align-center justify-center" style="height: 100vh">
        <v-sheet width="400" class="mx-auto">
            <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Login form</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-alert
                        v-if="showAlert"
                        :color="varient"                                                
                        :text="message"
                        ></v-alert>
                     <v-form fast-fail @submit.prevent="login">
                            <v-text-field
                              v-model="username"
                              name="username"
                              label="Username"
                              type="text"
                              placeholder="username"
                              required
                           ></v-text-field>
                           
                            <v-text-field
                              v-model="password"
                              name="password"
                              label="Password"
                              type="password"
                              placeholder="password"
                              required
                           ></v-text-field>
                           <v-btn block type="submit" class="fill-width" color="primary" value="log in">Login</v-btn>
                      </v-form>
                        <div class="mt-2">
                            <p class="text-body-2">Don't have an account? <a href="#">Sign Up</a></p>
                        </div>
                     </v-card-text>
                  </v-card>


        </v-sheet>
    </div>
  </template>
  
  <script>
  export default {
    name: "LoginForm",
    data() {
      return {
        username: "",
        password: "",
        showAlert: false,
        varient: "success",
        message: "Hi"
      };
    },
    methods: {
        login: function() {
            fetch('/api/v1/user/auth', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({"email": this.username, "password": this.password})
            })
            .then(response => response.json().then(jdata=> ({response: response, data: jdata})))
            .then(({response, data}) => {
                if(!response.ok){
                    throw new Error(`Error ${response.status}: ${data.msg}`)
                } else {
                    this.message = "Login Successful, Redirecting"
                    this.showAlert = true
                    this.varient = "success"
                    sessionStorage.setItem("name", data.profile.name)
                    sessionStorage.setItem("email", data.profile.email)
                    sessionStorage.setItem("role", data.profile.role)
                    sessionStorage.setItem("token", data.auth.authToken)
                    if(data.profile.role == "admin"){
                      this.$router.push({name:"AdminDashboard"})
                    }
                    
                }
            })
            .catch(error => {
                this.message = error.message
                this.showAlert = true
                this.varient = "error"
            })
        },
    },
  };
  </script>
  