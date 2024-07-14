<template>
  <div class="about">
    <h1>This is an about page {{ this.data }}</h1>
    <input type="text" placeholder="say something" v-model="this.data">
    <button @click="anchit">send request</button> <br>
    message: {{ this.text }}, with status: {{ this.result }}!
    
  </div>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return{
      data: null,
      result: null,
      text: null
    }
  },
  methods:{
    anchit(){
      console.log(this.data)
      axios
        .put("http://localhost:5000/test", 
          {
            demo: this.data
          }
        )
        .then((anchit) => {
          console.log(anchit);
          this.result = anchit.status;
          this.text = anchit.data.message;
        })
        .catch((error) => {
          console.log(error);
        });

    }
  }
}
</script>
