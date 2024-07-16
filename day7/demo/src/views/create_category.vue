<template>
<input type="text" placeholder="name goes here" v-model="this.name">
<input type="text" placeholder="desc goes here" v-model="this.desc">
<!-- <input type="text" placeholder="name goes here" v-model="this.name" :value="this.old_name">
<input type="text" placeholder="desc goes here" v-model="this.desc" :value="this.old_desc"> -->
<button @click="create_category"> create</button>
</template>
<script>
import axios from "axios";
export default {
    name: 'CreateCategory',
    data(){
        return{
            name: null,
            desc: null,
            token: null,
            role: null,
            old_name: null,
            old_desc: null
        }
    },
    created(){
        this.token = localStorage.getItem("token");
        this.role = localStorage.getItem("role");
        if (this.token != null){
            if (this.role != "admin"){
                this.$router.push("/login");
            }
            this.$router.push("/login");
        }
        // getn category
    },
    methods: {
        create_category(){
            console.log(this.token);
            axios.post("http://localhost:5000/api/category", {
                name: this.name,
                description: this.desc
            }, {headers: {
                Authorization: this.token,
            }})
                
            .then((response) => {
                console.log(response);
                if (response.status == 201){
                    this.$router.push("/");
                }
            })
            .catch((error) => {
                console.log("catched: ", error);
            });
        }
    }
}

</script>
