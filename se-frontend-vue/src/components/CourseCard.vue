<template>
    <v-card shaped class="rounded-card mx-auto mt-5" max-width="344">
        <v-card-title class="text-center">{{course.name}}</v-card-title>
        <v-divider />
        <v-card-text>
            <!-- <p class="text-justify">{{ course.description }}</p> -->
            <v-table density="compact">
            <tbody>
                <tr>
                    <td class="text-left">Course Code:</td>
                    <td class="text-right">{{course.id}}</td>
                </tr>
                <tr>
                    <td class="text-left">Difficulty Score:</td>
                    <td class="text-right">{{ course.difficulty_rating }}</td>
                </tr>
                <!-- <tr>
                    <td class="text-left">Description:</td>
                    <td class="text-justify">{{ course.description }}</td>
                </tr> -->
                <tr>
                    <td class="text-left">Pre-requisites:</td>
                    <td class="text-right"><p v-for="(c, index) in course.pre_req">{{ c }},</p></td>
                </tr>
                <tr>
                    <td class="text-left">Co-requisites:</td>
                    <td class="text-right"><p v-for="(c, index) in course.co_req">{{ c }},</p></td>
                </tr>
            </tbody>
        </v-table>
        </v-card-text>        
        <v-card-actions>              
            <v-btn
                block
                class="text-none text-black"
                color="primary"      
                variant="outlined"
                :to="{name: 'CourseView', params: {id: course.id}}"
            >View More Info</v-btn>
              
        </v-card-actions>
    </v-card>
</template>

<script>
export default{
    name: "CourseCard",
    props: {
        course: Object,        
    }
}
</script>