<template>
    <v-container>
      <v-card elevation="2">
        <v-data-table
          :headers="headers"
          :items="courses"
          :group-by="groupBy"
          items-per-page="25"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Courses</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
            </v-toolbar>
          </template>
  
          <template v-slot:item.instructors="{ item }">
            <p class="mt-2" v-for="x in item.instructors">{{ x.name }}</p>
          </template>
  
          <template v-slot:item.actions="{ item }">
            <v-btn color="primary" :to="{ name: 'IMCourseFeedback', params: { courseId: item.id }}">  
              View Feedback
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    data: () => ({
      groupBy: [
        {
          key: 'level',
        },
      ],
      search: '',
      courses: [
      {
      id: 'CS001',
      name: 'Introduction to Programming',
      difficulty_rating: 'Intermediate',
      instructors: [
        { name: 'Instructor 1', email: 'instructor1@example.com' },
        { name: 'Instructor 2', email: 'instructor2@example.com' },
      ],
      level: 'foundation',
    },
    {
      id: 'CS002',
      name: 'Introduction to Programming',
      difficulty_rating: 'Intermediate',
      instructors: [
        { name: 'Instructor 1', email: 'instructor1@example.com' },
        { name: 'Instructor 2', email: 'instructor2@example.com' },
      ],
      level: 'diploma',
    },
    {
      id: 'CS003',
      name: 'Web Development Basics',
      difficulty_rating: 'Intermediate',
      instructors: [
        { name: 'Instructor 3', email: 'instructor3@example.com' },
        { name: 'Instructor 4', email: 'instructor4@example.com' },
      ],
      level: 'diploma',
    },
    {
      id: 'CS004',
      name: 'Web Development Basics',
      difficulty_rating: 'Intermediate',
      instructors: [
        { name: 'Instructor 3', email: 'instructor3@example.com' },
        { name: 'Instructor 4', email: 'instructor4@example.com' },
      ],
      level: 'diploma',
    }
      ],
      headers: [
        {
          title: 'Course Code',
          align: 'start',
          key: 'id',
        },
        { title: 'Name', key: 'name' },
        { title: 'Difficulty Rating', key: 'difficulty_rating' },
        { title: 'Instructors', key: 'instructors' },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
    }),
  
    created() {
      this.initialize();
    },
  
    methods: {
      initialize: async function () {
        let token = sessionStorage.getItem('token');
        await fetch('/api/v1/courses/all', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
          .then((response) =>
            response.json().then((jdata) => ({ response: response, data: jdata }))
          )
          .then(({ response, data }) => {
            if (!response.ok) {
              throw new Error(`Error ${response.status}: ${data.msg}`);
            }
            this.courses = data;
          })
          .catch((error) => {
            console.log(error);
          });
      },
  
      
    },
  };
  </script>