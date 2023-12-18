<template>
    <v-container fill-height fluid class="down-top-padding">
      <v-row>        
        <v-col cols="3" lg="4">
          <v-card elevation="3">
            <v-card-title>{{ cards[0].title }}</v-card-title>
            <v-divider />
            <v-list>
              <v-list-item>                
                <span class="float-left">Total</span>
                <span class="float-right">{{ cards[0].data.total }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Foundation</span>
                <span class="float-right">{{ cards[0].data.foundation }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Diploma</span>
                <span class="float-right">{{ cards[0].data.diploma }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">BSc</span>
                <span class="float-right">{{ cards[0].data.bsc }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">BS</span>
                <span class="float-right">{{ cards[0].data.bs }}</span>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title>{{ cards[1].title }}</v-card-title>
            <v-divider />
            <v-list>
              <v-list-item>                
                <span class="float-left">Total</span>
                <span class="float-right">{{ cards[1].data.total }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Foundation</span>
                <span class="float-right">{{ cards[1].data.foundation }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Diploma</span>
                <span class="float-right">{{ cards[1].data.diploma }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Degree</span>
                <span class="float-right">{{ cards[1].data.degree }}</span>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-btn color="primary" block :to="{name: 'AdminsCourseList'}">View all courses</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title>{{ cards[2].title }}</v-card-title>
            <v-divider />
            <v-list>
              <v-list-item>                
                <span class="float-left">Admins</span>
                <span class="float-right">{{ cards[2].data.superadmins }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Course Team Members</span>
                <span class="float-right">{{ cards[2].data.ctm }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">IITM Management</span>
                <span class="float-right">{{ cards[2].data.management }}</span>
              </v-list-item>
            </v-list>
            <v-table>
            </v-table>
            <v-card-actions>
              <v-btn color="primary" block :to="{ name: 'AdminsList' }">View all admins</v-btn>
            </v-card-actions>
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
            data: {}
          },
          {
            title: "Course Details",
            data: {}
          },
          {
            title: "Non-Student Details",
            data: {}
          }
        ]
      }
    },

    mounted: async function () 
    {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/stats/general', {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          },
          
      })
      .then(response => response.json().then(jdata=> ({response: response, data: jdata})))
      .then(({response, data}) => {
          if(!response.ok){
              throw new Error(`Error ${response.status}: ${data.msg}`)
          }
          this.cards[0].data = data['students']
          this.cards[1].data = data['courses']
          this.cards[2].data = data['admins']
      })
      .catch(error => {                                
          console.log(error)
      })
    },    
  }
  
  </script>