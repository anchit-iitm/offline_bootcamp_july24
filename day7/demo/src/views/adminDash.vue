<template>
    <h1>categories</h1>
    <table>
        <thead>
            <th>id</th>
            <th>name</th>
            <th>description</th>
            <th>created on</th>
            <th>actions</th>
        </thead>
        <tbody>
            <tr v-for="cat in category" :key="cat.id">
                <td>{{cat.id}}</td>
                <td>{{cat.name}}</td>
                <td>{{cat.description}}</td>
                <td>{{cat.created_at}}</td>
                <td>
                    <button v-if="cat.delete==false" @click="deletecategory(cat.id)">delete</button>
                </td>
            </tr>
        </tbody>        
    </table>
    <h1>products</h1>
    <table>
        <thead>
            <th>id</th>
            <th>name</th>
            <th>description</th>
            <th>created on</th>
            <th>actions</th>
        </thead>
        <tbody>
            <tr v-for="cat in products" :key="cat.id">
                <td>{{cat.id}}</td>
                <td>{{cat.name}}</td>
                <td>{{cat.description}}</td>
                <td>{{cat.created_at}}</td>
                <td>
                
                    <button v-if="cat.delete==false" @click="deletecategory(cat.id)">delete</button>
                </td>
            </tr>
        </tbody>        
    </table>
</template>

<script>
import axios from 'axios';
export default{
    name: 'AdminDash',
    data(){
        return{
            token: null,
            category: null,
            products: null
        }
    },
    created(){
        this.token = localStorage.getItem("token");
        if (this.token){
            this.getcatedata();
            this.getproddata();
        }
    },
    methods: {
        getcatedata(){
            axios.get('http://localhost:5000/api/category', {
                headers: {
                    Authorization: this.token
                }
        })
            .then((response) => {
                console.log(response);
                this.category = response.data.data;
            })
            .catch(error =>
                console.log(error)
            )
        },
        deletecategory(Id){
            axios.delete(`http://localhost:5000/api/category/${Id}`, {
                headers: {
                    Authorization: this.token
                }
        })
            .then((response) => {
                console.log(response);
                this.getcatedata();
            })
            .catch(error =>
                console.log(error)
            )
        },
        getproddata(){
            axios.get('http://localhost:5000/api/product', {
                headers: {
                    Authorization: this.token
                }
        })
            .then((response) => {
                console.log(response);
                this.products = response.data.data;
                console.log(this.products[0].delete);
            })
            .catch(error =>
                console.log(error)
            )
        }
    }
}

</script>