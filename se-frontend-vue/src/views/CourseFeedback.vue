<template>
  <div>
    <div>
    <h1>Course Feedback</h1>
        <h3>Code: {{ courseData.code }}</h3>
        <h4>Name: {{ courseData.name }}</h4>
        <p>Description: {{ courseData.description }}</p>
    </div>
    <div v-if="feedbacks.length === 0">No feedback available.</div>
    <div v-else>
      <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-card">
        <p>Description: {{ feedback.description }}</p>
        <p>Rating: {{ feedback.rating }}</p>
        <div class="feedback-meta">
          <p>Time: {{ feedback.time }}</p>
          <p>Likes: {{ feedback.likes }}</p>
          <p>Dislikes: {{ feedback.dislikes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      courseData: {
          "code": "CS101",
          "name": "Introduction to Computer Science",
          "description": "An introductory course covering fundamental concepts in computer science.",
          "difficulty_rating": 3.5,
          "level": "foundation",
          "dp_or_ds": "both",
          "credits": 3
  },
      feedbacks: [{
          "id": 1,
          "user": {"email": "user1@example.com"},
          "rating": 4.5,
          "description": "Great course! Enjoyed the material.",
          "time": "2023-01-15T08:30:00.000Z",
          "likes": 10,
          "dislikes": 2
  },
  {
    "id": 2,
    "user": {"email": "user2@example.com"},
    "rating": 3.8,
    "description": "The content was interesting, but the assignments were challenging.",
    "time": "2023-01-16T10:45:00.000Z",
    "likes": 5,
    "dislikes": 1
  }],
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

        
        this.feedbacks = feedbackData
        this.courseData = courseData
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Add your styling for feedback cards here */
.feedback-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 10px 10px 10px; /* Adjust the top and bottom margin */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Add box shadow for a shadowed appearance */
}
.feedback-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

</style>