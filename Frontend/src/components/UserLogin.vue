<template>
  <div>
    <div class="ting">
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
        <div class="signup">
          <br>
          New? <router-link to="/usignup" id="signup-link">Signup</router-link>
        </div>
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
  name: "UserLogin",
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
        const response = await axios.post('http://127.0.0.1:5000/userlogin', {
          username: this.username,
          password: this.password
        });

        if (response.status === 200) {
          console.log('Login successful', response.data);
          this.$router.push(`/udashboard/${response.data.id}/${response.data.username}`);
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
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
.animate {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 1s, transform 1s;
}
.ting {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: repeating-linear-gradient(
    -55deg, /* Slightly steeper angle for a more dynamic look */
    #333333 0%,   /* Dark Charcoal */
    #4F4F4F 15%,  /* Medium Dark Grey */
    #828282 30%,  /* Medium Grey */
    #bdc3c7 45%,  /* Light Grey */
    #ecf0f1 60%,  /* Very Light Grey */
    #bdc3c7 75%,  /* Light Grey */
    #828282 90%,  /* Medium Grey */
    #4F4F4F 100%  /* Medium Dark Grey */
  );
    background-size: cover;
    background-position: center;
    font-family: 'Dancing Script', cursive;
  }

  .login-form {
  background: rgba(255, 255, 255, 0.75); /* Slightly more opaque for better readability */
  padding: 40px; 
  border-radius: 15px; /* Smoother border radius */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Softer shadow for a subtle depth */
  max-width: 400px;
  width: 90%; /* Responsive width */
  margin: auto; /* Center align the form */
  display: flex; /* Use flexbox to align children */
  flex-direction: column; /* Stack children vertically */
  align-items: center; /* Center-align children horizontally */
  justify-content: center;
  transform: translateY(0); /* Start at normal position */
  opacity: 1; /* Start fully visible */
  transition: transform 0.5s ease-out, opacity 0.5s ease-in;
}

.login-form:hover {
  transform: translateY(-10px); /* Slight raise effect on hover */
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2); /* Increased shadow on hover for a lifting effect */
}

.login-form form {
  display: flex;
  flex-direction: column;
}

.login-form input[type="text"],
.login-form input[type="password"] {
  width: 100%;
  padding: 12px; 
  margin: 10px 0;
  border: 2px solid #efefef; 
  border-radius: 8px; 
  font-family: 'Arial', sans-serif;
  font-size: 16px; 
  transition: border-color 0.3s;
}

.login-form input[type="text"]:focus,
.login-form input[type="password"]:focus {
  border-color: #ff5e96; 
  outline: none; 
}

.login-form button {
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

.login-form button:hover {
  background-color: #55D0FF; 
}
  .header, .middle, .footer {
    text-align: center;
    font-size: 1.2rem;
    font-weight: 700;
  }
  
  .footer {
    position: fixed;
    bottom: 0;
    left:0;
    padding: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease-out, transform 1s ease-out;
  }
  
  .footer.animate {
  opacity: 1;
  transform: translateY(0);
}

  .top {
    position: fixed;
    top: 0;
    left:0;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transform: translateY(20px); 
    transition: all 1s ease-out;
    font-size: 2.0rem;
    font-weight: 500;
    opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease-out, transform 1s ease-out;
  }
   .top.animate {
  opacity: 1;
  transform: translateY(0);
}
  .logo {
    position: fixed;
    top:0;
    left: 0px; 
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    transform: translateY(20px); 
    transition: all 1s ease-out;
  }
  
  .logo img {
    height: 50px; 
  }
   .logo.animate {
  opacity: 1;
  transform: translateY(0);
}
  .btn {
    background-color: #13e02bb9;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .btn:hover {
    background-color: #55D0FF;
  }
</style>
