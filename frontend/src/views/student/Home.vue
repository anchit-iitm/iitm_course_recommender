<template>
  <v-app>
    <v-main>

      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Current Courses ({{ current_courses.length }})</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list>
                  <v-list-item v-for="(item, index) in current_courses" append-icon="mdi-information" :to="{name: 'CourseView', params: {id: item.id}}">
                    <v-list-item-title>{{ item.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.id }}</v-list-item-subtitle>                    
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Recommended Courses ({{ upcoming_term.length }})</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list>
                  <v-list-item v-for="(item, index) in upcoming_term" append-icon="mdi-information" :to="{name: 'CourseView', params: {id: item.id}}">
                    <v-list-item-title>{{ item.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.id }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

        </v-row>
      </v-container>
      <v-container>
        <v-card>
          <v-card-title>Recommended Future Courses</v-card-title>
          <v-card-text>
            <div id="cy" class="cy"></div>
          </v-card-text>
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
      current_courses: [],
      current_degree_level: "",
      dp: false,
      max_courses: 2,
      upcoming_term: [],


      nodes: [],
      edges: []
    }
  },

  methods: {
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
          data.bio.current_courses.forEach((courseCode) => this.getCourseInfo(courseCode).then(r => this.current_courses.push(r)))
          this.current_degree_level = data.bio.current_degree_level
          this.max_courses = data.bio.maximum_courses_in_a_term
          console.log("Profile Data Fetched")
        })
        .catch(error => {
          console.log(error)
        })
    },

    getRecommendations: async function () {
      let token = sessionStorage.getItem("token")
      await fetch('/api/v1/recommender', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
        .then(({ response, data }) => {
          data.upcoming_term.forEach((courseCode) => this.getCourseInfo(courseCode).then(r => this.upcoming_term.push(r)))

          let i = 0
          data.matrix_order.forEach((aCombination) => {
            let node = {
              data: {
                id: i,
                name: "",
                description: "",
                active: true,
                width: 0,
                height: 0
              },
            }

            aCombination.forEach((subject) => { node.data.name += subject.name + "\n" }),
            node.data.width = node.data.name.split('\n').reduce(function (a, b) {return a.length > b.length ? a : b;}).length*10
            node.data.height = (node.data.name.match(/\n/g) || []).length * 20

              this.nodes.push(node)
            i++
          })

          let x = 0
          this.nodes.forEach((aNode) => {
            this.edges.push(
              { data: { source: x, target: x + 1, label: `Term ${x+2}` } }
            )
            x++
          })
          this.edges.pop()          
          this.drawGraph()
          console.log("Recommendations Fetched")
        })
        .catch(error => {
          console.log(error)
        })
    },

    drawGraph() {
      cydagre(cytoscape);
      const cy = cytoscape({
        container: document.getElementById("cy"),
        boxSelectionEnabled: false,
        autounselectify: true,        
        style: cytoscape
          .stylesheet()
          .selector("node")
          .css({
            shape: "roundrectangle",
            height: "data(height)",
            width: "data(width)",
            "background-color": (node) =>
              node.data("active") ? "white" : "white",
            color: (node) => (node.data("active") ? "black" : "black"),
            "border-color": "black",
            "border-width": 1,
            "border-radius": 4,
            content: "data(name)",
            "text-wrap": "wrap",
            "text-valign": "center",
            "text-halign": "center",
          })
          .selector("edge")
          .css({
            // http://js.cytoscape.org/#style/labels
            //label: "data(label)", // maps to data.label
            "text-outline-color": "white",
            "text-outline-width": 3,
            "text-valign": "top",
            "text-halign": "left",
            // https://js.cytoscape.org/demos/edge-types/
            "curve-style": "bezier",
            width: 1,
            "target-arrow-shape": "triangle",
            "line-color": "black",
            "target-arrow-color": "black",
          }),
        elements: {
          nodes: this.nodes,
          edges: this.edges,
        },
        layout: {
          name: "dagre",
          spacingFactor: 1.5,
          rankDir: "TB",
          animate:true,
          fit: true,
        },
      });

      cy.userZoomingEnabled(false);
    },
  },

  mounted: async function () {
    this.getProfile()
    this.getRecommendations()
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
}
</style>