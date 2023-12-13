<template>
    <v-container>
        <v-card elevation="2">
            <v-card-title>Course Team</v-card-title>
            <template v-slot:text>
                <v-text-field
                    v-model="search"
                    label="Search"
                    prepend-inner-icon="mdi-magnify"
                    single-line
                    variant="outlined"
                    hide-details
                ></v-text-field>
            </template>
            <v-data-table :items="ctm" density="compact" :search="search">
                <template v-slot:item="row">
                    <tr>
                        <td width="40%">{{row.item.id}}</td>
                        <td width="40%">{{row.item.name}}</td>                        
                        <td>
                            <v-btn class="mx-2" height="80%" fab dark small color="blue" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn class="mx-2" height="80%" fab dark small color="red" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-trash-can</v-icon>
                            </v-btn>
                        </td>
                    </tr>
                </template>
            </v-data-table>
        
            <v-card-actions>
                <v-btn color="primary">Add Course Team Member</v-btn>
            </v-card-actions>
        </v-card>        
    </v-container>

    <v-container>
        <v-card>
            <v-card-title>Management Team</v-card-title>
            <v-data-table :items="im">
                <template v-slot:item="row">
                    <tr>
                        <td width="40%">{{row.item.id}}</td>
                        <td width="40%">{{row.item.name}}</td>                        
                        <td>
                            <v-btn class="mx-2" fab dark small color="blue" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn class="mx-2" fab dark small color="red" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-trash-can</v-icon>
                            </v-btn>
                        </td>
                    </tr>
                </template>
            </v-data-table>
        
            <v-card-actions>
                <v-btn color="primary">Add Management Team Member</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>

    <v-container>
        <v-card>
            <v-card-title>Administrators</v-card-title>
            <v-data-table :items="adm">
                <template v-slot:item="row">
                    <tr>
                        <td width="40%">{{row.item.id}}</td>
                        <td width="40%">{{row.item.name}}</td>                        
                        <td>
                            <v-btn class="mx-2" fab dark small color="blue" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn class="mx-2" fab dark small color="red" @click="onButtonClick(row.item)">
                                <v-icon dark>mdi-trash-can</v-icon>
                            </v-btn>
                        </td>
                    </tr>
                </template>
            </v-data-table>

            <v-card-actions>
                <v-btn color="primary">Add Administrator</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
    
</template>


<script>

    export default {
        data: function() {
            return {
                search: '',
                ctm: [],
                im: [],
                adm: []
            }
        },
        mounted: async function(){
            let token = sessionStorage.getItem("token")
            await fetch('/api/v1/admin', {
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
                for (var item in data) {
                    if (data[item].role == "ctm"){
                        this.ctm.push({
                            id: data[item].email,
                            name: data[item].name,
                        })
                    } else if (data[item].role == "im"){
                        this.im.push({
                            id: data[item].email,
                            name: data[item].name,
                            
                        })
                    } else if (data[item].role == "admin"){
                        this.adm.push({
                            id: data[item].email,
                            name: data[item].name                            
                        })
                    }
                }
            })
            .catch(error => {
                if(error.message.includes("Token has expired")){
                    // toastr.error("Re-login required, token has expired", 'Error')
                    // this.$router.push("/relogin")
                }
                // toastr.error(error.message, 'Error')
                //console.log(error)
            })
        }
    }
</script>