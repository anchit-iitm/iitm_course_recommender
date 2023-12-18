<template>
    <v-container>
        <v-card flat>
            <v-card-title class="text-h5">{{ course.id }} - {{ course.name }}</v-card-title>
            <v-divider />
            <v-card-text>
                <v-row>
                    <v-col cols="12" md="4">
                        <v-card>
                            <v-card-title>About the course</v-card-title>
                            <v-card-text>
                                <v-list>
                                    <v-list-item>
                                        <v-list-item-title>Level: {{ course.level }}</v-list-item-title>
                                    </v-list-item>
                                    <v-list-item class="text-justify">{{ course.description }}</v-list-item>
                                </v-list>

                            </v-card-text>
                        </v-card>
                    </v-col>

                    <v-col cols="12" md="4">
                        <v-card>
                            <v-card-title>Average Difficulty</v-card-title>
                            <v-card-text class="text-center">
                                <v-progress-circular :rotate="360" :size="200" :width="35"
                                    :model-value="course.difficulty_rating * 10"
                                    :color="course.difficulty_rating >= 7 ? 'red' : course.difficulty_rating > 3 ? 'warning' : 'green'">
                                    <template v-slot:default>{{ course.difficulty_rating }}</template>
                                </v-progress-circular>

                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col cols="12" md="4">
                        <v-card>
                            <v-card-title>Instructors</v-card-title>
                            <v-card-text>
                                <v-list>
                                    <!-- <span v-if="course.instructors.length == 0" class="text-center text-h6">No instructors assigned!</span> -->
                                    <v-list-item v-for="(ins, index) in course.instructors"
                                        prepend-avatar="@/assets/user2.png">
                                        <v-list-item-title>{{ ins.name }}</v-list-item-title>
                                        <v-list-item-subtitle>{{ ins.email }}</v-list-item-subtitle>
                                    </v-list-item>
                                </v-list>

                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="12" md="12">
                        <v-card flat>
                            <v-card-title>Feedbacks</v-card-title>
                            <v-card-text>
                                <v-dialog v-model="dialog" max-width="500px">
                                    <template v-slot:activator="{ props }">
                                        <v-btn color="primary" dark class="mb-2" v-bind="props"
                                            v-if="submittedFeedback == -1">
                                            Give Feedback
                                        </v-btn>
                                        <v-btn color="secondary" dark class="mb-2" v-bind="props"
                                            v-if="submittedFeedback > -1">
                                            View Feedback
                                        </v-btn>
                                    </template>
                                    <v-card>
                                        <v-card-title class="text-h6">Submit Your Feedback</v-card-title>
                                        <v-card-text>
                                            <v-container>
                                                <v-row>
                                                    <v-textarea v-model="editedFeedback.description"
                                                        label="What do you think about this course?"></v-textarea>
                                                </v-row>
                                                <v-row>
                                                    <v-slider v-model="editedFeedback.rating" class="align-center" max="10"
                                                        min="0" hide-details thumb-label="always" color="primary">
                                                        <template v-slot:append>
                                                            <v-text-field v-model="editedFeedback.rating" hide-details
                                                                single-line density="compact" type="number"
                                                                style="width: 70px"></v-text-field>
                                                        </template>
                                                    </v-slider>
                                                </v-row>

                                            </v-container>
                                        </v-card-text>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="secondary" variant="text" @click="close"
                                                v-if="submittedFeedback == -1">
                                                Cancel
                                            </v-btn>
                                            <v-btn color="primary" variant="text" @click="save"
                                                v-if="submittedFeedback == -1">
                                                Save
                                            </v-btn>
                                            <v-btn color="red" variant="text" @click="deleteFeedback"
                                                v-if="submittedFeedback > -1">
                                                Delete
                                            </v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                                <v-card v-for="feedback in feedbacks" :key="feedback.id" class="mt-4">
                                    <V-row>
                                        <v-col cols="12" md="8">
                                            <v-list density="compact">
                                                <v-list-item prepend-avatar="@/assets/user.png" :title="feedback.poster"
                                                    :subtitle="feedback.time"></v-list-item>
                                                <v-divider width="40%" class="ml-5 mt-1"></v-divider>
                                                <v-list-item>{{ feedback.description }}</v-list-item>
                                            </v-list>
                                            <v-card-actions>
                                                <v-btn flat>
                                                    <v-icon>mdi-thumb-up-outline</v-icon>
                                                    <div>{{ feedback.likes }}</div>
                                                </v-btn>
                                                <v-btn flat>
                                                    <v-icon>mdi-thumb-down-outline</v-icon>
                                                    <div>{{ feedback.dislikes }}</div>
                                                </v-btn>
                                            </v-card-actions>
                                        </v-col>
                                        <v-col cols="12" md="4" class="d-flex align-center justify-center">
                                            <v-progress-circular :rotate="360" :size="100" :width="15"
                                                :model-value="feedback.rating * 10"
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
    </v-container>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
    data() {
        return {
            id: "",
            course: "",
            dialog: false,
            submittedFeedback: -1,
            editedFeedback: {
                description: "",
                rating: 0
            },
            defaultFeedback: {
                description: "",
                rating: 0
            },
            feedbacks: [{
                "id": 1,
                "poster": "user1@example.com",
                "rating": 4.5,
                "description": "Great course! Enjoyed the material.",
                "time": "2023-01-15T08:30:00.000Z",
                "likes": 10,
                "dislikes": 2
            },
            {
                "id": 2,
                "poster": "user2@example.com",
                "rating": 3.8,
                "description": "The content was interesting, but the assignments were challenging.",
                "time": "2023-01-16T10:45:00.000Z",
                "likes": 5,
                "dislikes": 1
            }],
        }
    },

    watch: {
        dialog(val) {
            val || this.close()
        },
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
        }
    },

    mounted: async function () {
        let route = useRoute()
        this.id = route.params.id
        this.getCourseInfo()
    },
}
</script>