<template>
    <v-container fill-height fluid class="down-top-padding">
      <v-row>        
        <v-col cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title class="text-center">{{ cards[0].title }}</v-card-title>
            <v-divider />
            <v-table>
              <tbody>
                <tr>
                  <td>Total</td>
                  <td>{{ cards[0].data.total }}</td>
                </tr>
                <tr>
                  <td>Foundation</td>
                  <td>{{ cards[0].data.foundation }}</td>
                </tr>
                <tr>
                  <td>Diploma</td>
                  <td>{{ cards[0].data.diploma }}</td>
                </tr>
                <tr>
                  <td>BSc</td>
                  <td>{{ cards[0].data.bsc }}</td>
                </tr>
                <tr>
                  <td>BS</td>
                  <td>{{ cards[0].data.bs }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card>
        </v-col>

        <v-col cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title class="text-center">{{ cards[1].title }}</v-card-title>
            <v-divider />
            <v-table>
              <tbody>
                <tr>
                  <td>Total</td>
                  <td>{{ cards[1].data.total }}</td>
                </tr>
                <tr>
                  <td>Foundation</td>
                  <td>{{ cards[1].data.foundation }}</td>
                </tr>
                <tr>
                  <td>Diploma</td>
                  <td>{{ cards[1].data.diploma }}</td>
                </tr>
                <tr>
                  <td>Degree</td>
                  <td>{{ cards[1].data.degree }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card>
        </v-col>

        <v-col cols="3" lg="4">          
          <v-card elevation="3">
            <v-card-title class="text-center">{{ cards[2].title }}</v-card-title>
            <v-divider />
            <!-- <v-card-text>{{ item.text }}</v-card-text> -->
            <v-table>
              <tbody>
              <tr>
                <td>Admins</td>
                <td>{{ cards[2].data.superadmins }}</td>
              </tr>
              <tr>
                <td>Course Team Members</td>
                <td>{{ cards[2].data.ctm }}</td>
              </tr>
              <tr>
                <td>IITM Management</td>
                <td>{{ cards[2].data.management }}</td>
              </tr>
            </tbody>
            </v-table>
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