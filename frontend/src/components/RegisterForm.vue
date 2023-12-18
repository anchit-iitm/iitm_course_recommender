<template>  
    <div class="d-flex align-center justify-center" style="height: 90vh">
            <v-sheet width="400" class="mx-auto">
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                      <v-toolbar-title>Sign In form</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                      <!-- <v-alert
                      v-if="showAlert"
                      :color="varient"                                                
                      :text="message"
                      ></v-alert> -->
                      <v-form fast-fail @submit.prevent="register">
                            <v-text-field
                            v-model="name"
                            name="name"
                            label="Name"
                            type="text"
                            placeholder="John Doe"
                            required
                            ></v-text-field>

                            <v-text-field
                            v-model="email"
                            name="email"
                            label="Email"
                            type="email"
                            placeholder="email@example.com"
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

                            <v-btn block type="submit" class="fill-width" color="primary">
                            Sign In
                            </v-btn>
                        </v-form>
                      <div class="mt-2">
                        Already have an account? <router-link to="/">Login</router-link>
                      </div>
                    </v-card-text>
                </v-card>
            </v-sheet>
        </div>
      </template>
      
      <script>
      export default {
        name: "RegisterForm",
        data() {
          return {        
            name: "",
            email: "",
            password: "",
            };
        },
        methods: {
            register: async function() {

                await fetch("/api/v1/user/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: this.name,
                        email: this.email,
                        password: this.password,
                    })
                })
                .then(response => response.json().then(jdata=> ({response: response, data: jdata})))
                .then(({response, data}) => {
                    if(!response.ok){
                        throw new Error(`${data.message}`)
                    } else {
                        this.$router.push({name:"Login"})
                    }
                })
                .catch(error => {
                    this.$root.vtoast.show({message: error.message, color: 'error'})
                })
            },
        },
      };
      </script>