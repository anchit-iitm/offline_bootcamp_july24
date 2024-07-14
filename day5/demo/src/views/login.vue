<template>
  <h1>login page</h1>
  <input type="text" placeholder="email" v-model="this.email" />
  <input type="text" placeholder="password" v-model="this.password" />
  <button @click="login">Login</button>
</template>
<script>
import axios from "axios";
export default {
  // name: 'Login'
  data() {
    return {
      email: null,
      password: null,
    };
  },
  methods: {
    login() {
      axios
        .post("http://localhost:5000/api/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          if (response.status == 200) {
            console.log(response);

            localStorage.setItem("token", response.data.authToken);
            localStorage.setItem("role", response.data.role);
            this.$router.push("/");
          }else{
            this.$router.push("/login");
          }
        })
        .catch((error) => {
          console.log("catched: ", error);
        });
    },
  },
};
</script>
<style></style>
