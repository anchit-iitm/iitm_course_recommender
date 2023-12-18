<template>
    <v-container>
      <!-- Course Information -->
      <v-container style="background-color: #1565C0; color: white;" class="text-center">
      <div>
        <h1>COURSE FEEDBACK</h1>
        <h2>{{ courseData.name }}</h2>
      </div>
    </v-container>
  
      <!-- Feedbacks -->
      <v-card v-for="feedback in feedbacks" :key="feedback.id" class="mt-4">
        <v-card-title>
          <v-icon prepend-icon>mdi-account</v-icon>{{ feedback.poster }}
        </v-card-title>
        <v-card-text>{{ feedback.description }}</v-card-text>
        <v-card-actions>
            <v-card-subtitle>
          <v-icon prepend-icon>{{ getStarIcon(feedback.rating) }}</v-icon>{{ feedback.rating }}
        </v-card-subtitle>
        <v-card-subtitle>
            <v-icon prepend-icon>{{ getLikeIcon() }}</v-icon>{{ feedback.likes }}
        </v-card-subtitle>
        <v-card-subtitle>
            <v-icon prepend-icon>{{ getDislikeIcon() }}</v-icon>{{ feedback.dislikes }}
        </v-card-subtitle>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>
  
  <script>
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
      getStarIcon(rating) {
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
  </script>