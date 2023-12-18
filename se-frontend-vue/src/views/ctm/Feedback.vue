<template>
  <v-container :key="id">
    <v-card flat>
      <v-card-title class="text-h5">
        <span class="float-left">{{ course.id }} - {{ course.name }}</span>
        <v-btn color="primary" class="float-right" @click="editCourse(course.id)">Edit Course Details</v-btn>
      </v-card-title>
      <v-divider />
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-card>
              <v-card-title>Course Description</v-card-title>
              <v-card-text>
                <v-list>                  
                  <v-list-item class="text-justify mt-2">{{ course.description }}</v-list-item>
                </v-list>

              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card>
              <v-card-title>Course Information</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>{{ course.level[0].toUpperCase() + course.level.slice(1) }}</v-list-item-title>
                    <v-list-item-subtitle>Level</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>{{ course.dp_or_ds == "dp" ? "Programming Course" : "Data Science Course"}}</v-list-item-title>
                    <v-list-item-subtitle>Course Category</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>{{ course.credits}}</v-list-item-title>
                    <v-list-item-subtitle>Credits</v-list-item-subtitle>
                  </v-list-item>
                </v-list>

              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card>
              <v-card-title>Average Difficulty</v-card-title>
              <v-card-text class="text-center">
                <v-progress-circular :rotate="360" :size="200" :width="35" :model-value="course.difficulty_rating * 10"
                  :color="course.difficulty_rating >= 7 ? 'red' : course.difficulty_rating > 3 ? 'warning' : 'green'">
                  <template v-slot:default>{{ course.difficulty_rating }}</template>
                </v-progress-circular>

              </v-card-text>
            </v-card>
          </v-col>          
        </v-row>

        <v-row>
          <v-col cols="12" md="12">
            <v-card flat>
              <v-card-title>Feedbacks ({{ feedbacks.length }})</v-card-title>
              <v-card-text>
                <v-card v-for="feedback in feedbacks" :key="feedback.id" class="mt-4">
                  <V-row>
                    <v-col cols="12" md="10">
                      <v-list density="compact">
                        <v-list-item prepend-avatar="@/assets/user.png" :title="feedback.poster"
                          :subtitle="feedback.time"></v-list-item>
                        <v-divider width="40%" class="ml-5 mt-1"></v-divider>
                        <v-list-item class="text-justify">{{ feedback.description }}</v-list-item>
                      </v-list>
                      <v-card-actions>
                        <v-btn flat disabled>
                          <v-icon>mdi-thumb-up-outline</v-icon>
                          <div>{{ feedback.likes }}</div>
                        </v-btn>
                        <v-btn flat disabled>
                          <v-icon>mdi-thumb-down-outline</v-icon>
                          <div>{{ feedback.dislikes }}</div>
                        </v-btn>
                      </v-card-actions>
                    </v-col>
                    <v-col cols="12" md="2" class="d-flex align-center justify-center">
                      <v-progress-circular :rotate="360" :size="100" :width="15" :model-value="feedback.rating * 10"
                        :color="feedback.rating >= 7 ? 'red' : feedback.rating > 3 ? 'warning' : 'green'">
                        <template v-slot:default>{{ feedback.rating }}</template>
                      </v-progress-circular>
                    </v-col>
                  </V-row>
                </v-card>

              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-dialog v-model="editDialog" max-width="600">
      <v-card>
        <v-card-title>Edit Course</v-card-title>
        <v-card-text>
          <v-text-field v-model="course.name" label="Name"></v-text-field>
          <v-textarea v-model="course.description" label="Description"></v-textarea>          
          <v-select v-model="course.level" :items="levelOptions" label="Level"></v-select>
          <v-select v-model="course.dp_or_ds" :items="dpOrDsOptions" label="DP or DS"></v-select>
          <v-text-field v-model="course.credits" label="Credits"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveChanges">Save Changes</v-btn>
          <v-btn color="secondary" @click="cancelEdit">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  data() {
    return {
      id: "",
      course: {level: "Hehe"},
      // dialog: false,
      editDialog: false,
      // editedCourseId: null,
      // editedName: '',
      // editedDescription: '',
      // editedLevel: null,
      // editedDpOrDs: null,
      // editedCredits: '',
      levelOptions: ['foundation', 'diploma', 'degree'],
      dpOrDsOptions: ['dp', 'ds'],
      submittedFeedback: -1,
      editedFeedback: {
        description: "",
        rating: 0
      },
      defaultFeedback: {
        description: "",
        rating: 0
      },
      feedbacks: [],
    }
  },

  watch: {
    dialog(val) {
      val || this.close()
    },

    '$route': {
      handler(newValue, oldValue) {        
        this.id = newValue.params.courseId
        this.getCourseInfo()
      }
      
    }
  },

methods: {
  close() {
    this.dialog = false
    this.$nextTick(() => {
      this.editedFeedback = Object.assign({}, this.defaultFeedback)
    })
  },
  save: async function () {
    let token = sessionStorage.getItem("token")
    await fetch(`/api/v1/course/${this.id}/feedback`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.editedFeedback)

    })
      .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
      .then(({ response, data }) => {
        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${data.message}`)
        }
        this.getCourseInfo()
        this.getAllFeedbacks()
        this.$root.vtoast.show({ message: "Feedback Submitted" })
      })
      .catch(error => {
        console.log(error)
      })
    this.close()
  },

  deleteFeedback: async function () {
    let token = sessionStorage.getItem("token")
    await fetch(`/api/v1/feedback/${this.submittedFeedback}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
    })
      .then(response => response.json().then(jdata => ({ response: response, data: jdata })))
      .then(({ response, data }) => {
        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${data.message}`)
        }
        this.$root.vtoast.show({ message: "Feedback Deleted", color: "warning" })
        this.getCourseInfo()
        this.getAllFeedbacks()
        this.submittedFeedback = -1
      })
      .catch(error => {
        console.log(error)
      })
    this.close()
  },

  getAllFeedbacks: async function () {
    let token = sessionStorage.getItem("token")
    await fetch(`/api/v1/course/${this.id}/feedback`, {
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
        this.feedbacks = data

        this.feedbacks.forEach((item) => {
          if (item.poster == sessionStorage.getItem('email')) {
            this.defaultFeedback.description = item.description
            this.defaultFeedback.rating = item.rating
            this.editedFeedback.description = item.description
            this.editedFeedback.rating = item.rating
            this.submittedFeedback = item.id
          }
        })
      })
      .catch(error => {
        console.log(error)
      })
  },

  getCourseInfo: async function () {
    let token = sessionStorage.getItem("token")
    await fetch('/api/v1/courses/' + this.id, {
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
        this.course = data
        this.getAllFeedbacks()
      })
      .catch(error => {
        console.log(error)
      })
  },
  editCourse(id) {
      this.editDialog = true;
    },
    async saveChanges() {
      try {
        let token = sessionStorage.getItem('token');
        const response = await fetch(`/api/v1/courses/${this.id}`, {
          method: 'PATCH',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.course.name,
            description: this.course.description,
            level: this.course.level,
            dp_or_ds: this.course.dp_or_ds,
            credits: this.course.credits,
          }),
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        this.$root.vtoast.show({message: "Course information updated"})
        // Close the edit dialog
        this.editDialog = false;
      } catch (error) {
        this.$root.vtoast.show({message: error.message, color: 'error'})
      }
    },

    cancelEdit() {
      this.editDialog = false;
    },
},

mounted: async function () {
  let route = useRoute()
  this.id = route.params.courseId
  this.getCourseInfo()
},
}
</script>

  <!-- <script>
  export default {
    data() {
      return {
        courseData: {
          "id": "CS101",
          "name": "Introduction to Computer Science",
          "description": "An introductory course covering fundamental concepts in computer science.",
          "difficulty_rating": 3.5,
          "level": "foundation",
          "dp_or_ds": "both",
          "credits": 3
        },
        feedbacks: [
          {
            "id": 1,
            "poster": "user1@example.com",
            "rating": 4.5,
            "description": "Great course! Enjoyed the material.",
            "likes": 10,
            "dislikes": 2
          },
          // Add more feedback objects as needed
        ],
      };
    },
    mounted() {
      this.initialize();
    },
    methods: {
      async initialize() {
        try {
          let token = sessionStorage.getItem('token');
          const courseId = this.$route.params.courseId;
  
          const feedbackResponse = await fetch(`/api/v1/course/${courseId}/feedback`, {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
  
          if (!feedbackResponse.ok) {
            throw new Error(`Error ${feedbackResponse.status}: ${feedbackResponse.statusText}`);
          }
  
          const courseResponse = await fetch(`/api/v1/courses/${courseId}`, {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
  
          if (!courseResponse.ok) {
            throw new Error(`Error ${courseResponse.status}: ${courseResponse.statusText}`);
          }
  
          const feedbackData = await feedbackResponse.json();
          const courseData = await courseResponse.json();
  
          this.feedbacks = feedbackData;
          this.courseData = courseData;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      getStarIcon() {
        return 'mdi-star-outline';
      },
      getLikeIcon() {
        return 'mdi-heart-outline';
      },
      getDislikeIcon() {
        return 'mdi-thumb-down-outline';
      },
    },
  };
  </script> -->