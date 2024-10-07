<template>
  <div>
  <div class="ting">
    <div class="top" v-bind:class="{ animate: animateElements }">
      <p>Welcome to UB's Library</p>
    </div>
    <div class="logo" v-bind:class="{ animate: animateElements }">
      <img src="../assets/logo.jpg" alt="UB's Library Logo">
    </div>
    <div class="signup-form" role="form" aria-label="Signup Form" v-bind:class="{ animate: animateElements }">
      <div class="header">
        <h1>Signup</h1>
      </div>
      <form @submit.prevent="signup">
        <div class="mb-3">
          <label for="fname" class="form-label">First name:</label>
          <input type="text" id="fname" name="fname" class="form-control" placeholder="Enter your first name" v-model="fname">
        </div>
        <div class="mb-3">
          <label for="lname" class="form-label">Last name:</label>
          <input type="text" id="lname" name="lname" class="form-control" placeholder="Enter your last name" v-model="lname">
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username:</label>
          <input type="text" id="username" name="username" class="form-control" placeholder="Enter your username" v-model="username">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input type="password" id="password" name="password" class="form-control" placeholder="Enter password" v-model="password">
        </div>
        <button type="submit" class="btn btn-info">Sign up</button>
      </form>
      <div class="login">
        <br>
        Already have an account? <router-link to="/ulogin" id="login-link">Login</router-link>
      </div>
    </div>
    <div class="footer" v-bind:class="{ animate: animateElements }">
        <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
      </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "UserSignup",
  data() {
    return {
      logo: require('@/assets/logo.jpg'), 
      fname: '',
      lname: '',
      username: '',
      password: '',
      animateElements: false,
      message: ''
    };
  },
  mounted() {
    this.triggerAnimation();
  },
  methods: {
    async signup() {
    const payload = {
    fname: this.fname,
    lname: this.lname,
    username: this.username,
    password: this.password
  };
  console.log("Sending payload:", payload);
  try {
    const response = await axios.post('http://localhost:5000/usersignup', payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    this.message = response.data.message;
    this.clearForm();
    this.$router.push({ path:'/ulogin' });
  } catch (error) {
    if (error.response) {
      this.message = error.response.data.error || 'An error occurred';
    } else {
      this.message = 'An error occurred';
    }
    console.error(error);
  }
},
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    clearForm() {
      this.fname = '';
      this.lname = '';
      this.username = '';
      this.password = '';
    }
  }
};
</script>

<style>
  .signup-form {
  background: rgba(255, 255, 255, 0.75); /* Slightly more opaque for better readability */
  padding: 20px; 
  border-radius: 15px; /* Smoother border radius */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Softer shadow for a subtle depth */
  max-width: 400px;
  width: 90%; /* Responsive width */
  margin: auto; /* Center align the form */
  display: flex; /* Use flexbox to align children */
  flex-direction: column; /* Stack children vertically */
  align-items: center; /* Center-align children horizontally */
  justify-content: center;
  z-index:1000;
  transform: translateY(0); 
  opacity: 1; 
  transition: transform 0.5s ease-out, opacity 0.5s ease-in;
}

.signup-form:hover {
  transform: translateY(-10px); /* Slight raise effect on hover */
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2); /* Increased shadow on hover for a lifting effect */
}

.signup-form form {
  display: flex;
  flex-direction: column;
}

.signup-form input[type="text"],
.signup-form input[type="password"] {
  width: 90%;
  padding: 12px; 
  margin: 10px 0;
  border: 2px solid #efefef; 
  border-radius: 8px; 
  font-family: 'Arial', sans-serif;
  font-size: 16px; 
  transition: border-color 0.3s;
}

.signup-form input[type="text"]:focus,
.signup-form input[type="password"]:focus {
  border-color: #ff5e96; 
  outline: none; 
}

.signup-form button {
  width: 100%;
  padding: 12px;
  margin-top: 20px; 
  background-color: #ff5e96; 
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.signup-form button:hover {
  background-color: #55D0FF; 
}
 
</style>
