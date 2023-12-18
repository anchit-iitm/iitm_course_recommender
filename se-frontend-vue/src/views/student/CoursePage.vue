<template>
    <v-container>
        <v-card>
            <v-card-title>{{ course.id }} - {{ course.name }}</v-card-title>
            <v-divider />
            <v-card-text>
                {{ course.description }}
                <br />
                <br />
                Difficulty Score: {{ course.difficulty_rating }}
                <br />
                <br />
                Level: {{ course.level }}

                <br><br><br>
                <p class="text-h6">Feedbacks</p>
                <div v-if="feedbacks.length === 0">No feedback available.</div>
                <div v-else>
                    <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-card">
                        <p>Description: {{ feedback.description }}</p>
                        <p>Rating: {{ feedback.rating }}</p>
                        <div class="feedback-meta">
                            <v-btn flat>
                                <v-icon>mdi-thumb-up-outline</v-icon>
                                <div>{{ feedback.likes }}</div>
                            </v-btn>
                            <v-btn flat>
                                <v-icon>mdi-thumb-down-outline</v-icon>
                                <div>{{ feedback.dislikes }}</div>
                            </v-btn>
                        </div>
                    </div>
                </div>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
    data() {
        return {
            id: "",
            course: "",
            feedbacks: [{
                "id": 1,
                "user": { "email": "user1@example.com" },
                "rating": 4.5,
                "description": "Great course! Enjoyed the material.",
                "time": "2023-01-15T08:30:00.000Z",
                "likes": 10,
                "dislikes": 2
            },
            {
                "id": 2,
                "user": { "email": "user2@example.com" },
                "rating": 3.8,
                "description": "The content was interesting, but the assignments were challenging.",
                "time": "2023-01-16T10:45:00.000Z",
                "likes": 5,
                "dislikes": 1
            }],
        }
    },

    mounted: async function () {
        let route = useRoute()
        this.id = route.params.id
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
            })
            .catch(error => {
                console.log(error)
            })
        

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
            })
            .catch(error => {
                console.log(error)
            })
    },
}
</script>


<style scoped>
/* Add your styling for feedback cards here */
.feedback-card {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 10px 10px 10px;
    /* Adjust the top and bottom margin */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    /* Add box shadow for a shadowed appearance */
}

.feedback-meta {
    display: flex;
    /* justify-content: space-between; */
    margin-top: 10px;
}
</style>