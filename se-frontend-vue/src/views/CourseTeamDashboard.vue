<template>
  <v-container fill-height fluid class="down-top-padding">
    <v-row>
      <v-col v-for="item in cards" :key="item.code" cols="3" lg="4">
        <v-card elevation="3">
          <v-card-title>{{ item.code }}</v-card-title>
          <v-divider />
          <v-card-text>
            <strong>Name:</strong> {{ item.name }}<br>
            <strong>Description:</strong> {{ item.description }}<br>
            <strong>Difficulty:</strong> {{ item.difficulty_rating }}<br>
            <strong>Level:</strong> {{ item.level }}<br>
            <strong>DP or DS:</strong> {{ item.dp_or_ds }}<br>
            <strong>Credits:</strong> {{ item.credits }}
          </v-card-text>
          <v-card-actions>
            <v-btn @click="editCourse(item.id)">Edit</v-btn>
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
        cards: [{
          id : 1,
          code: 'CS101',
          name: 'Introduction to Computer Science',
          description: 'An introductory course covering fundamental concepts in computer science.',
          difficulty_rating: 4.5,
          level: 'foundation',
          dp_or_ds: 'both',
          credits: 3,
        },
        {
          id : 1,
          code: 'MATH201',
          name: 'Calculus II',
          description: 'A continuation of Calculus I, focusing on advanced calculus topics.',
          difficulty_rating: 5.0,
          level: 'degree',
          dp_or_ds: 'both',
          credits: 4,
        }]
      }
    },
    created() {
    this.initialize();
  },

  methods: {
    initialize: async function () {
      try {
        let token = sessionStorage.getItem('token');
        const response = await fetch('/api/v1/courses/all', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        // Filter the courses based on the user's token
        this.courseList = data.filter((course) => {
          const instructors = course.instructors.map((ins) => ins.email);
          return instructors.includes(sessionStorage.getItem('email'));
        });
      } catch (error) {
          console.log(error);
      }
    },
  }
}
  
  </script>