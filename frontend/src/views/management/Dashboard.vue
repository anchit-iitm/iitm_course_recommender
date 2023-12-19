<template>
  <v-container fill-height fluid class="down-top-padding">
    <v-row>
      <v-col cols="3" lg="4">
        <v-card elevation="3">
          <v-card-title>{{ cards[0].title }}</v-card-title>
          <v-divider />
          <v-card-text class="d-flex justify-center">
            <Pie class="text-center text-justify" v-if="cards[0].loaded" :data="cards[0].cdata" :options="cards[0].options" />
          </v-card-text>
          <v-list>
              <v-list-item>                
                <span class="float-left">Foundation</span>
                <span class="float-right">{{ this.cards[0].cdata.datasets[0].data[0] }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Diploma</span>
                <span class="float-right">{{ this.cards[0].cdata.datasets[0].data[1] }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Degree</span>
                <span class="float-right">{{ this.cards[0].cdata.datasets[0].data[2] }}</span>
              </v-list-item>
            </v-list>
        </v-card>
      </v-col>

      <v-col cols="3" lg="4">
        <v-card elevation="3">
          <v-card-title>{{ cards[1].title }}</v-card-title>
          <v-divider />
          <v-card-text class="d-flex justify-center">
            <Pie class="text-center text-justify" v-if="cards[1].loaded" :data="cards[1].cdata" :options="cards[1].options" />
          </v-card-text>
          <v-list>
              <v-list-item>                
                <span class="float-left">Foundation</span>
                <span class="float-right">{{ this.cards[1].cdata.datasets[0].data[0] }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Diploma</span>
                <span class="float-right">{{ this.cards[1].cdata.datasets[0].data[1] }}</span>
              </v-list-item>
              <v-list-item>                
                <span class="float-left">Degree</span>
                <span class="float-right">{{ this.cards[1].cdata.datasets[0].data[2] }}</span>
              </v-list-item>
            </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  
<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Colors } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)
export default {
  components: {
    Pie
  },
  data() {
    return {
      cards: [
        {
          title: "Student Details",
          cdata: {
            labels: ["Foundation", "Diploma", "Degree"],
            datasets: [
              {
                backgroundColor: this.$chartColors.p3,
                data: [],
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          },
          loaded: false,

        },
        {
          title: "Course Details",
          cdata: {
            labels: ["Foundation", "Diploma", "Degree"],
            datasets: [
              {
                backgroundColor: this.$chartColors.p3,
                data: [],
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          },
          loaded: false,
        },
        {
          title: "Non-Student Details",
          data: {}
        }
      ]
    }
  },

  mounted: async function () {
    let token = sessionStorage.getItem("token")
    await fetch('/api/v1/stats/general', {
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
        this.cards[0].cdata.datasets[0].data = [data['students'].foundation, data['students'].diploma, data['students'].degree]
        this.cards[0].loaded = true
        this.cards[1].cdata.datasets[0].data = [data['courses'].foundation, data['courses'].diploma, data['courses'].degree]
        this.cards[1].loaded = true        
        this.cards[2].data = data['admins']
      })
      .catch(error => {
        console.log(error)
      })
  },
}

</script>