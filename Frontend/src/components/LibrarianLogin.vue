<template>
  <div>
    <div class="libd">
      <div class="top" v-bind:class="{ animate: animateElements }">
        <p>Welcome to UB's Library</p>
      </div>
      <div class="logo" v-bind:class="{ animate: animateElements }">
        <img src="../assets/logo.jpg" alt="UB's Library Logo">
      </div>
      <div class="login-form" role="form" aria-label="Login Form" v-bind:class="{ animate: animateElements }">
        <div class="header">
          <h1>Login</h1>
        </div>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Username:</label>
            <input type="text" id="username" name="username" class="form-control" placeholder="Enter your username" v-model="username">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input type="password" id="password" name="password" class="form-control" placeholder="Enter password" v-model="password">
          </div>
          <button type="submit" class="btn btn-info">Log in</button>
        </form>
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div class="footer" v-bind:class="{ animate: animateElements }">
        <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: "LibrarianLogin",
  data() {
    return {
      logo: require('@/assets/logo.jpg'),
      username: '',
      password: '',
      animateElements: false,
      errorMessage: ''  // To display error messages to the user
    };
  },
  mounted() {
    this.triggerAnimation();
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/llogin', {
          username: this.username,
          password: this.password
        });

        if (response.status === 200) {
          console.log('Login successful', response.data);
          this.$router.push(`/ldashboard/${response.data.id}/${response.data.username}`);
        } else {
          this.errorMessage = 'Login failed. Please check your credentials.';
        }
      } catch (error) {
        console.error('Login failed', error);
        this.errorMessage = error.response ? error.response.data.error : 'An unexpected error occurred.';
      }
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    }
  }
};
</script>

<style>
.libd {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
   
    background: repeating-linear-gradient(
    55deg, /* Slightly steeper angle for a more dynamic look */
    #0077B6 0%,   /* Vibrant blue */
    #0096C7 15%,  /* Bright cerulean */
    #48CAE4 30%,  /* Soft sky blue */
    #ADE8F4 45%,  /* Pale blue */
    #CAF0F8 60%,  /* Very light blue */
    #ADE8F4 75%,  /* Pale blue */
    #48CAE4 90%,  /* Soft sky blue */
    #0096C7 100%  /* Bright cerulean */);
    background-size: cover;
    background-position: center;
    font-family: 'Dancing Script', cursive;
  }

.info-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.info-block {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  flex: 1;
  min-width: 300px;
}

.info-block h3 {
  margin-top: 0;
}

.info-block input {
  width: 95%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.info-block ul {
  list-style: none;
  padding: 0;
}

.info-block li {
  margin-bottom: 10px;
}

.info-block li h4 {
  margin: 0;
}

.info-block li p {
  margin: 5px 0 0;
}

</style>