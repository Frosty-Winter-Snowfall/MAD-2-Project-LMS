<template>
  <div>
  <div class=peep>
    <div class="top" v-bind:class="{ animate: animateElements }">
        <p>Welcome to UB's Library</p>
      </div>
      <div class="logo" v-bind:class="{ animate: animateElements }">
        <img src="../assets/logo.jpg" alt="UB's Library Logo">
      </div>
    <div class="header">
      <div class="login-form" role="form" aria-label="Login Form" v-bind:class="{ animate: animateElements }">
        <p>Wanna read books?</p>
        <div class="middle">
          <router-link to="/ulogin">
            <button type="submit" name="action" value="login" class="btn btn-info">Log in</button>
          </router-link>
          <br>
          <br>
          <router-link to="/usignup">
            <button type="submit" name="action" value="signup" class="btn btn-info">Signup</button>
          </router-link>
          <br>
          <p>Are you the Librarian?</p>
          <router-link to="/llogin">
            <button type="submit" name="action" value="llogin" class="btn btn-info">Librarian Log in</button>
          </router-link>
        </div>
      </div>
    </div>
     <div class="footer" v-bind:class="{ animate: animateElements }">
        <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
      </div>
  </div>
  </div>
</template>


<script>
export default {
  name: "LoginOrSignup",
  data() {
    return {
      logo: require('@/assets/logo.jpg'),
      animateElements: false  // Ensure this property is declared
    };
  },
  mounted() {
    this.triggerAnimation();
  },
  methods: {
    triggerAnimation() {
      // Set a slight delay to ensure the DOM is fully ready
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

.peep {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;


    background: linear-gradient(
        55deg, /* Gradient direction from top to bottom */
        #005f73 0%,   /* Rich Navy Blue */
        #00b4d8 20%,  /* Moderate Blue */
        #90e0ef 40%,  /* Soft Blue */
        #bdc3c7 60%,  /* Silver */
        #ecf0f1 80%,  /* Clouds */
        #4F4F4F 100%  /* Silver */
    );

    
    background-size: cover;
    background-position: center;
    font-family: 'Dancing Script', cursive;
    
  }


 
  .login-form {
    background: rgba(255, 255, 255, 0.458);
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    width: 100%;
    transform: translateY(20px); 
    opacity: 0; 
    transition: all 1s ease-out;
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
    transform: translateY(20px); 
    transition: all 1s ease-out;
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
  
  .btn {
    background-color: #0080BF;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .btn:hover {
    background-color: #0080BF;
  }
</style>
