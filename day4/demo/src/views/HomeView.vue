<template>
  <div class="home">
    <button>Send request</button>
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import { onBeforeMount } from 'vue';

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
