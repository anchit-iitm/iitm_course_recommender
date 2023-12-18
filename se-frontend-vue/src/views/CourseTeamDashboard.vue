<template>
  <v-container fill-height fluid class="down-top-padding">
    <v-row>
      <v-col v-for="item in cards" :key="item.id" cols="3" lg="4">
        <v-card elevation="3">
          <v-card-title>{{ item.id }}</v-card-title>
          <v-divider />
          <v-card-text>
            <strong>Name:</strong> <u>{{ item.name }}</u><br>
            <strong>Description:</strong> {{ item.description }}<br>
            <strong>Difficulty:</strong> {{ item.difficulty_rating }}<br>
            <strong>Level:</strong> <a style="text-transform: capitalize;">{{ item.level }}</a><br>
            <strong>DP or DS:</strong> <a style="text-transform: uppercase;">{{ item.dp_or_ds }}</a><br>
            <strong>Credits:</strong> {{ item.credits }}
          </v-card-text>
          <v-card-actions>
            <v-btn @click="editCourse(item.id)">Edit</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="editDialog" max-width="600">
      <v-card>
        <v-card-title>Edit Course</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedName" label="Name"></v-text-field>
          <v-text-field v-model="editedDescription" label="Description"></v-text-field>
          <!-- <v-text-field v-model="editedDifficulty" label="Difficulty"></v-text-field> -->
          <v-select
            v-model="editedLevel"
            :items="levelOptions"
            label="Level"
          ></v-select>
          <v-select
            v-model="editedDpOrDs"
            :items="dpOrDsOptions"
            label="DP or DS"
          ></v-select>
          <v-text-field v-model="editedCredits" label="Credits"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="saveChanges">Save Changes</v-btn>
          <v-btn @click="cancelEdit">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
  
  
  <script>
  export default {
    data(){
      return {
        cards: [],
        editDialog: false,
        editedCourseId: null,
        editedName: '',
        editedDescription: '',
        editedLevel: null,
        editedDpOrDs: null,
        editedCredits: '',
        levelOptions: ['foundation', 'diploma', 'degree'],
        dpOrDsOptions: ['dp', 'ds'],
        card: [{
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
    async initialize () {
      let token = sessionStorage.getItem("token")
            await fetch('/api/v1/courses/all', {
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
                this.cards = data
                // console.log('Fetched Data:', this.cards);
                
                // let courses_list = data.filter((item) => {                    
                //     let instructors = item.instructors.filter((ins) => ins.email)
                //     return instructors.includes(sessionStorage.getItem("token"))
                //   })
                
            })
            .catch(error => {                                
                console.log(error)
            })
    },
    editCourse(id) {
      const course = this.cards.find(item => item.id === id);
      this.editedCourseId = id;
      this.editedName = course.name;
      // this.editedDifficulty = course.difficulty_rating;
      this.editedLevel = course.level;
      this.editedDpOrDs = course.dp_or_ds;
      this.editedCredits = course.credits;
      this.editedDescription = course.description;
      this.editDialog = true;
    },
    async saveChanges() {
      try {
        let token = sessionStorage.getItem('token');
        const response = await fetch(`/api/v1/courses/${this.editedCourseId}`, {
          method: 'PATCH',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
body: JSON.stringify({
            name: this.editedName,
            description: this.editedDescription,
            level: this.editedLevel,
            dp_or_ds: this.editedDpOrDs,
            credits: this.editedCredits,
          }),
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        // Fetch updated course data after saving changes
        await this.initialize();

        // Close the edit dialog
        this.editDialog = false;
      } catch (error) {
          console.error(error);
      }
    },

    cancelEdit() {
      this.editDialog = false;
    },
  }
}
  
  </script>