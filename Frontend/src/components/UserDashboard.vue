<template>
  <div class="kale">
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
       <i class="fas fa-bars" aria-hidden="true"></i>
       <span v-if="isCollapsed" class="sr-only">Expand</span>
       <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
      <li><router-link :to="`/mybooks/${id}`">My Books</router-link></li>
      <li><router-link :to="{ path: '/borrowbooks', query: { id: id, username: username } }">Borrow Books</router-link></li>
      </ul>
    </div>
    <div class="top"  :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Welcome {{ username }}</h1>
      <div class="account">
        <button class="account-btn" aria-haspopup="true" aria-expanded="false">
          <i class="bi bi-backpack-fill"></i>
        </button>
        <div class="account-actions" role="menu">
        <div class="button-group">
          <form @submit.prevent="logout">
            <button type="submit" class="edit-button" role="menuitem">Logout</button>
          </form>
          
            <button type="submit" class="delete-acc" @click="deleteAccount(this.id)" role="menuitem">Delete Account</button>
          
          </div>
        </div>
      </div>
    </div>


    <div class="main-content" :class="{ animate: animateElements }" role="main">
    <div class="lwelcome-card" :class="{ animate: animateElements }">
        <h2>Welcome Back, {{ username }} !</h2>
        <p>What will you be doing today?</p>
        <ul>
          <li><router-link :to="{ path: '/borrowbooks', query: { id: id, username: username } }">Borrow new books perhaps?</router-link></li>
          <li>Check out the latest arrivals below !</li>
        </ul>
      </div>
      <div class="linfo-blocks">
        <div class="linfo-block" :class="{ animate: animateElements }">
        <h3>Library Books</h3>
          <input type="text" v-model="bookSearch" placeholder="Search books...">
          <ul>
            <li v-for="book in filteredBooks" :key="book.id">
              <h4>{{ book.name }}</h4>
              <p>Author: {{ book.author }}</p>
              <p>{{ book.content }}</p>
              
            </li>
          </ul>
        </div>
        <div class="linfo-block" :class="{ animate: animateElements }">
          <h3>Sections</h3>
          <input type="text" v-model="sectionSearch" placeholder="Search sections...">
          <ul>
            <li v-for="section in filteredSections" :key="section.id">
              <h4>{{ section.name }} :</h4>
              <p>Number of books: {{ section.book_count }}</p>
              <ul>
                <li v-for="book in section.books" :key="book.name">
                  <p>Book: {{ book.name }} by {{ book.author }}</p>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer" :class="{ animate: animateElements }">
        <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      books: [],
      sections: [],
      bookSearch: '',
      sectionSearch: '',
      success:false,
      message:''
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchBooks();
    this.fetchSections();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async logout() {
    try {
      await axios.post('http://localhost:5000/logout');
      localStorage.removeItem('token'); 
      this.$router.push('/'); 
    } catch (error) {
      console.error('Error logging out:', error);
    }
  },
  async deleteAccount() {
      try {
        const response = await axios.post(`http://localhost:5000/deleteaccount/${this.id}`);
        this.message = response.data.message;
        localStorage.removeItem('token');
        this.$router.push('/');
        this.success = true;
      } catch (error) {
        console.error('Error deleting account:', error);
        this.message = 'Error.';
        this.success = false;
      }
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    async fetchBooks() {
      try {
        const response = await axios.get('http://localhost:5000/books');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async fetchSections() {
      try {
        const response = await axios.get('http://localhost:5000//sections');
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    }
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book => 
        book.name.toLowerCase().includes(this.bookSearch.toLowerCase()) ||
        book.author.toLowerCase().includes(this.bookSearch.toLowerCase())
      );
    },
    filteredSections() {
      return this.sections.filter(section => 
        section.name.toLowerCase().includes(this.sectionSearch.toLowerCase())
      );
    }
  }
};
</script>


<style>
.kale {
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

.animate {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 1s ease-out, transform 1s ease-out;
}

.sidebar {
  
  z-index: 1000;
    width: 20%;
    height: 67vh;
    position: fixed;
    background-color: ##ffc6e2;
    padding: 15px;
    box-shadow: 0 0 10px rgb(6, 6, 6);
    overflow: auto;
    font-family: cursive;
    font-weight: 600;
    font-size: 25px;
    color: #000000;
    line-height: 2;
    margin-top: 0;
    margin-bottom: 100px;
    top: 120px;
    bottom: 100px;
    left: 0;
    transition: all 1s ease-out;
    opacity: 0;
    transform: translateY(20px);
    }

.sidebar.animate {
  opacity: 1;
  transform: translateY(0);
}

.sidebar.collapsed {
  width: 50px;
  
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 24px; 
  cursor: pointer;  
  padding: 10px; 
}

.welcome-message {
  font-size: 35px;
  margin-left: 15px;
  
}

.account {
  position: relative;
}

.account-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.account-actions {
  display: none;
  position: unset;
  right: 0;
  top: 100%;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.account-btn:focus + .account-actions,
.account-actions:hover {
  display: block;
}

.welcome-card {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 20px;
  transition: all 1s ease-out;
    opacity: 0;
    transform: translateY(20px);
}

.welcome-card.animate {
  opacity: 1;
  transform: translateY(0);
}

.info-blocks {
   display: flex;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: nowrap;
    flex-direction: row;
  
}

.info-block {
  max-height: 150px;
  width: 50%; 
  margin: 10px 0;
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
  overflow-y: auto;
}

.info-block.animate {
  opacity: 1;
  transform: translateY(0);
}
.info-block input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.info-block ul {
  
  padding: 0;
}

.info-block li {
    margin-left: 50px;
    margin-bottom: 10px;
}
.info-block h3 {
  margin-top: 0;
}

.info-block input {
  width: 90%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.main-content {
  margin-left: 22%;
  padding: 15px;
  overflow: auto;
  opacity: 0; /* Initial state for animation */
  transform: translateY(20px);
  transition: opacity 1s ease-out, transform 1s ease-out;
}
.main-content.animate {
  opacity: 1;
  transform: translateY(0);
}
.footer {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease-out, transform 1s ease-out;
}

.footer.animate {
  opacity: 1;
  transform: translateY(0);
}

.delete-acc{
    z-index:1000;
    background-color: #e90f0f;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
}
.delete-acc:hover {
  background-color: #55D0FF;
}
</style>
