<template>
  <v-app>
    <v-main>
      <v-container>
        <p class="text-h5 text-center">Recommended Courses</p>
        <v-row>
          <v-col v-for="(item, index) in upcoming_term" cols="12" md="4">
            <v-row>
              <v-col>
                <CourseCard :course="item" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <p class="text-h5 text-center">Current Courses</p>
        <v-row>
          <v-col v-for="(item, index) in current_courses" cols="12" md="4">
            <v-row>
              <v-col>
                <CourseCard :course="item" />
              </v-col>
            </v-row>
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
      completed_courses: [],
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
      let data = ""
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
          this.completed_courses = data.bio.completed_courses
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
                width: 300,
              },
            }

            aCombination.forEach((subject) => { node.data.name += subject.name + "\n" }),

              this.nodes.push(node)
            i++
          })

          let x = 0
          this.nodes.forEach((aNode) => {
            this.edges.push(
              { data: { source: x, target: x + 1 } }
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
            height: 40,
            width: "data(width)",
            "background-color": (node) =>
              node.data("active") ? "green" : "white",
            color: (node) => (node.data("active") ? "white" : "black"),
            "border-color": "gray",
            "border-width": 3,
            "border-radius": 4,
            content: "data(name)",
            "text-wrap": "wrap",
            "text-valign": "center",
            "text-halign": "center",
          })
          .selector("edge")
          .css({
            // http://js.cytoscape.org/#style/labels
            // label: "data(label)", // maps to data.label
            "text-outline-color": "white",
            "text-outline-width": 3,
            "text-valign": "top",
            "text-halign": "left",
            // https://js.cytoscape.org/demos/edge-types/
            "curve-style": "bezier",
            width: 3,
            "target-arrow-shape": "triangle",
            "line-color": "gray",
            "target-arrow-color": "gray",
          }),
        elements: {
          nodes: this.nodes,
          edges: this.edges,
        },
        layout: {
          name: "dagre",
          spacingFactor: 1.5,
          rankDir: "TB",
          fit: true,
        },
      });
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
  width: 960px;
}
</style>